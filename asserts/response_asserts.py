import logging
from typing import Any, Dict, Iterable, Optional
import requests


logger = logging.getLogger(__name__)


class ResponseAsserts:

    @staticmethod
    def assert_is_response(response: Any) -> None:
        assert isinstance(response, requests.Response), f"Expected requests.Response, got {type(response)}"

    @staticmethod
    def assert_status(response: requests.Response, expected_status: int) -> None:
        ResponseAsserts.assert_is_response(response)
        assert isinstance(expected_status, int), f"expected_status must be int, got {type(expected_status)}"

        if response.status_code != expected_status:
            logger.error(ResponseAsserts._debug_response(response))
        assert response.status_code == expected_status, ResponseAsserts._debug_response(response)

    @staticmethod
    def assert_content_type_contains(response: requests.Response, expected: str) -> None:
        ResponseAsserts.assert_is_response(response)
        assert isinstance(expected, str), f"expected must be str, got {type(expected)}"

        content_type = response.headers.get("Content-Type", "")
        if expected not in content_type:
            logger.error(ResponseAsserts._debug_response(response))
        assert expected in content_type, f"Unexpected Content-Type: {content_type}\n{ResponseAsserts._debug_response(response)}"

    @staticmethod
    def assert_body_not_empty(response: requests.Response) -> None:
        ResponseAsserts.assert_is_response(response)
        body = response.text or ""
        if body.strip() == "":
            logger.error(ResponseAsserts._debug_response(response))
        assert body.strip() != "", f"Response body is empty\n{ResponseAsserts._debug_response(response)}"

    @staticmethod
    def parse_json(response: requests.Response) -> Dict[str, Any]:
        ResponseAsserts.assert_is_response(response)
        ResponseAsserts.assert_body_not_empty(response)

        try:
            data = response.json()
        except ValueError:
            logger.error(ResponseAsserts._debug_response(response))
            raise AssertionError(f"Response is not valid JSON\n{ResponseAsserts._debug_response(response)}")

        if not isinstance(data, dict):
            logger.error(ResponseAsserts._debug_response(response))
            raise AssertionError(f"Expected JSON object (dict), got {type(data)}. Data: {data}\n{ResponseAsserts._debug_response(response)}")

        return data

    @staticmethod
    def assert_json_has_keys(data: Dict[str, Any], expected_keys: Iterable[str]) -> None:
        assert isinstance(data, dict), f"data must be dict, got {type(data)}"
        assert expected_keys is not None, "expected_keys must not be None"

        missing = [key for key in expected_keys if key not in data]
        assert not missing, f"Missing keys: {missing}. Got: {data}"

    @staticmethod
    def assert_field_type(data: Dict[str, Any], field: str, expected_type: type) -> None:
        assert isinstance(data, dict), f"data must be dict, got {type(data)}"
        assert isinstance(field, str), f"field must be str, got {type(field)}"
        assert isinstance(expected_type, type), f"expected_type must be type, got {type(expected_type)}"

        assert field in data, f"Field '{field}' is missing. Got: {data}"
        value = data[field]
        assert isinstance(value, expected_type), f"Field '{field}' type mismatch: expected {expected_type}, got {type(value)}. Value: {value}"

    @staticmethod
    def assert_token_present(data: Dict[str, Any]) -> None:
        ResponseAsserts.assert_json_has_keys(data, ["token"])
        ResponseAsserts.assert_field_type(data, "token", str)
        assert data["token"], "Token is empty"

    @staticmethod
    def _debug_response(response: requests.Response) -> str:
        req = response.request
        return (
            f"\nREQUEST: {req.method} {req.url}"
            f"\nREQ_HEADERS: {dict(req.headers)}"
            f"\nREQ_BODY: {req.body}"
            f"\nRESPONSE_STATUS: {response.status_code}"
            f"\nRESP_HEADERS: {dict(response.headers)}"
            f"\nRESP_BODY: {response.text}\n"
        )