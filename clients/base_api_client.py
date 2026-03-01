from typing import Optional, Callable, Dict, Any
import time
import logging
import requests

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(self, base_url: str, timeout: int = 10, retries: int = 2, retry_backoff: float = 0.5):
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url must be a non-empty string")
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout must be a positive int")
        if not isinstance(retries, int) or retries < 0:
            raise ValueError("retries must be int >= 0")
        if not isinstance(retry_backoff, (int, float)) or retry_backoff < 0:
            raise ValueError("retry_backoff must be number >= 0")

        self.base_url = base_url.rstrip("/")
        self._token: Optional[str] = None
        self._token_provider: Optional[Callable[[], str]] = None
        self.timeout = timeout
        self.retries = retries
        self.retry_backoff = float(retry_backoff)

    def set_token(self, token: str) -> None:
        if not isinstance(token, str) or not token:
            raise ValueError("token must be a non-empty string")
        self._token = token

    def set_token_provider(self, provider: Callable[[], str]) -> None:
        if not callable(provider):
            raise TypeError("provider must be callable")
        self._token_provider = provider

    @staticmethod
    def _mask_headers(headers: Dict[str, str]) -> Dict[str, str]:
        masked = dict(headers)
        cookie = masked.get("Cookie")
        if cookie and "token=" in cookie:
            masked["Cookie"] = "token=***"
        auth = masked.get("Authorization")
        if auth:
            masked["Authorization"] = "***"
        return masked

    @staticmethod
    def _mask_json(payload: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if payload is None:
            return None
        masked = dict(payload)
        for key in ("password", "token"):
            if key in masked and isinstance(masked[key], str):
                masked[key] = "***"
        return masked

    @staticmethod
    def _truncate(text: str, limit: int = 2000) -> str:
        if text is None:
            return ""
        if len(text) <= limit:
            return text
        return text[:limit] + "...(truncated)"

    def _format_exchange(
            self,
            method: str,
            url: str,
            *,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response: Optional[requests.Response] = None,
            error: Optional[Exception] = None,
    ) -> str:
        safe_headers = self._mask_headers(headers or {})
        safe_json = self._mask_json(json)

        parts = [
            f"REQUEST: {method} {url}",
            f"REQ_HEADERS: {safe_headers}",
            f"REQ_PARAMS: {params}",
            f"REQ_JSON: {safe_json}",
        ]

        if response is not None:
            parts.extend([
                f"RESPONSE_STATUS: {response.status_code}",
                f"RESP_HEADERS: {dict(response.headers)}",
                f"RESP_BODY: {self._truncate(response.text)}",
            ])

        if error is not None:
            parts.append(f"ERROR: {repr(error)}")

        return "\n" + "\n".join(parts) + "\n"

    def request(
            self,
            method: str,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        if not isinstance(method, str) or not method.strip():
            raise TypeError("method must be a non-empty string")
        if not isinstance(path, str) or not path.startswith("/"):
            raise TypeError("path must be a string starting with '/'")
        if params is not None and not isinstance(params, dict):
            raise TypeError("params must be dict or None")
        if json is not None and not isinstance(json, dict):
            raise TypeError("json must be dict or None")
        if headers is not None:
            if not isinstance(headers, dict):
                raise TypeError("headers must be dict or None")
            for k, v in headers.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise TypeError("headers must be Dict[str, str]")

        url = f"{self.base_url}{path}"

        merged_headers: Dict[str, str] = {}
        if self._token:
            merged_headers["Cookie"] = f"token={self._token}"
        if headers:
            merged_headers.update(headers)

        def _do_request() -> requests.Response:
            return requests.request(
                method,
                url,
                params=params,
                json=json,
                headers=merged_headers,
                timeout=self.timeout,
            )

        attempts = self.retries + 1
        last_exc: Optional[Exception] = None

        for attempt in range(1, attempts + 1):
            try:
                response = _do_request()


                if response.status_code in (401, 403) and self._token_provider:
                    logger.warning(
                        "AUTH FAILED. Re-auth and retry once.%s",
                        self._format_exchange(method, url, params=params, json=json, headers=merged_headers, response=response)
                    )
                    new_token = self._token_provider()
                    self.set_token(new_token)
                    merged_headers["Cookie"] = f"token={self._token}"
                    response = _do_request()

                    if response.status_code >= 400:
                        logger.warning(
                            "REQUEST FAILED AFTER RE-AUTH.%s",
                            self._format_exchange(method, url, params=params, json=json, headers=merged_headers, response=response)
                        )
                    return response

                if response.status_code >= 500 and attempt < attempts:
                    logger.warning(
                        "5xx RETRY attempt %s/%s.%s",
                        attempt, attempts,
                        self._format_exchange(method, url, params=params, json=json, headers=merged_headers, response=response)
                    )
                    time.sleep(self.retry_backoff * attempt)
                    continue

                if response.status_code >= 400:
                    logger.warning(
                        "REQUEST RETURNED ERROR STATUS.%s",
                        self._format_exchange(method, url, params=params, json=json, headers=merged_headers, response=response)
                    )

                return response

            except requests.exceptions.RequestException as e:
                last_exc = e
                logger.warning(
                    "REQUEST EXCEPTION attempt %s/%s.%s",
                    attempt, attempts,
                    self._format_exchange(method, url, params=params, json=json, headers=merged_headers, error=e)
                )
                if attempt < attempts:
                    time.sleep(self.retry_backoff * attempt)
                    continue
                raise RuntimeError(f"Request failed: {method} {url}. Error: {e}") from e

        raise RuntimeError(f"Request failed: {method} {url}. Error: {last_exc}")