from asserts.response_asserts import ResponseAsserts
from data.booking_payloads import (
    valid_auth_credentials,
    invalid_auth_credentials_wrong_password,
    invalid_auth_credentials_empty_password,
)


def test_auth_success_returns_token(rb_api):
    creds = valid_auth_credentials()
    response = rb_api.auth(creds["username"], creds["password"])

    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    ResponseAsserts.assert_token_present(data)


def test_auth_wrong_password_returns_no_token(rb_api):
    creds = invalid_auth_credentials_wrong_password()
    response = rb_api.auth(creds["username"], creds["password"])

    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    assert "token" not in data, f"Token should not be present for invalid creds. Got: {data}"


def test_auth_empty_password_returns_no_token(rb_api):
    creds = invalid_auth_credentials_empty_password()
    response = rb_api.auth(creds["username"], creds["password"])

    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    assert "token" not in data, f"Token should not be present for empty password. Got: {data}"