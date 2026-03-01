from typing import Any, Dict, Iterable, Optional

import requests


class ResponseAsserts:
    @staticmethod
    def debug_response(
            response: requests.Response,
            *,
            title: str = "HTTP exchange",
            max_body: int = 2000,
    ) -> str:
        req = getattr(response, "request", None)

        method = getattr(req, "method", None)
        url = getattr(req, "url", None)
        req_headers = dict(getattr(req, "headers", {}) or {})
        req_body = getattr(req, "body", None)

        resp_headers = dict(getattr(response, "headers", {}) or {})
        resp_body = response.text if getattr(response, "text", None) is not None else ""

        def _truncate(text: str, limit: int) -> str:
            if text is None:
                return ""
            if len(text) <= limit:
                return text
            return text[:limit] + "...(truncated)"

        return (
            f"\n{title}"
            f"\nREQUEST: {method} {url}"
            f"\nREQ_HEADERS: {req_headers}"
            f"\nREQ_BODY: {_truncate(str(req_body), max_body)}"
            f"\nRESPONSE_STATUS: {response.status_code}"
            f"\nRESP_HEADERS: {resp_headers}"
            f"\nRESP_BODY: {_truncate(resp_body, max_body)}\n"
        )

    @staticmethod
    def assert_status(response: requests.Response, expected_status: int) -> None:
        assert response.status_code == expected_status, ResponseAsserts.debug_response(
            response,
            title=f"Unexpected status. Expected={expected_status}, got={response.status_code}",
        )

    @staticmethod
    def assert_content_type_contains(response: requests.Response, expected: str) -> None:
        content_type = response.headers.get("Content-Type", "")
        assert expected in content_type, (
                f"Unexpected Content-Type. Expected to contain: {expected}. Got: {content_type}"
                + ResponseAsserts.debug_response(response, title="Content-Type mismatch")
        )

    @staticmethod
    def assert_json_has_keys(data: Dict[str, Any], expected_keys: Iterable[str]) -> None:
        missing = [k for k in expected_keys if k not in data]
        assert not missing, f"Missing keys: {missing}. Got keys: {list(data.keys())}. Full: {data}"

    @staticmethod
    def assert_token_present(data: Dict[str, Any]) -> None:
        assert "token" in data, f"Token field is missing. Full: {data}"
        assert isinstance(data["token"], str), f"Token must be str. Got: {type(data['token'])}. Full: {data}"
        assert data["token"], f"Token is empty. Full: {data}"

    @staticmethod
    def safe_json(response: requests.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            raise AssertionError(
                "Response body is not valid JSON."
                + ResponseAsserts.debug_response(response, title="JSON decode failed")
            )