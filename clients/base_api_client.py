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
        if not base_url:
            raise ValueError("base_url must not be empty")

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
                    logger.warning(f"AUTH FAILED: {method} {url} status={response.status_code}. Re-auth and retry once.")
                    new_token = self._token_provider()
                    self.set_token(new_token)
                    merged_headers["Cookie"] = f"token={self._token}"
                    response = _do_request()
                    return response

                if response.status_code >= 500 and attempt < attempts:
                    logger.warning(f"5xx RETRY: {method} {url} status={response.status_code} attempt {attempt}/{attempts}")
                    time.sleep(self.retry_backoff * attempt)
                    continue
                return response

            except requests.exceptions.RequestException as e:
                last_exc = e
                logger.warning(f"REQUEST FAILED: {method} {url} attempt {attempt}/{attempts} error={e}")
                if attempt < attempts:
                    time.sleep(self.retry_backoff * attempt)
                    continue
                raise RuntimeError(f"Request failed: {method} {url}. Error: {e}") from e

        raise RuntimeError(f"Request failed: {method} {url}. Error: {last_exc}")