class ResponseAsserts:

    @staticmethod
    def _debug_response(response):
        req = response.request
        return (
            f"\nREQUEST: {req.method} {req.url}"
            f"\nREQ_HEADERS: {dict(req.headers)}"
            f"\nREQ_BODY: {req.body}"
            f"\nRESPONSE_STATUS: {response.status_code}"
            f"\nRESP_HEADERS: {dict(response.headers)}"
            f"\nRESP_BODY: {response.text}\n"
        )

    @staticmethod
    def assert_status(response, expected_status):
        assert response.status_code == expected_status, \
            ResponseAsserts._debug_response(response)

    @staticmethod
    def assert_content_type_json(response):
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, \
            ResponseAsserts._debug_response(response)

    @staticmethod
    def assert_json_has_keys(data, expected_keys):
        missing = [key for key in expected_keys if key not in data]
        assert not missing, f"Missing keys: {missing}. Got: {data}"

    @staticmethod
    def assert_token_present(data):
        assert "token" in data, "Token field is missing in response"
        assert isinstance(data["token"], str), "Token is not a string"
        assert data["token"], "Token is empty"

    @staticmethod
    def assert_error_field_present(data):
        assert "reason" in data, f"No error field in response: {data}"