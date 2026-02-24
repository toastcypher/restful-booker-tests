from asserts.response_asserts import ResponseAsserts
from data.booking_payloads import valid_auth_credentials


def test_auth_success_returns_token(rb_api):
    creds = valid_auth_credentials()
    response = rb_api.auth(creds["username"], creds["password"])

    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    ResponseAsserts.assert_token_present(data)