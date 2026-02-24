import json
import requests

from config import BASE_URL
from asserts.response_asserts import ResponseAsserts
from data.booking_payloads import valid_booking_payload, booking_payload_missing_field


def test_create_booking_missing_required_field_returns_error(rb_api):
    payload = booking_payload_missing_field("lastname")
    response = rb_api.create_booking(payload)

    assert response.status_code in (400, 500), ResponseAsserts._debug_response(response)


def test_create_booking_invalid_json_returns_error():
    url = f"{BASE_URL}/booking"
    headers = {"Content-Type": "application/json"}
    bad_json = '{"firstname": "A", "lastname":'  # намеренно битый JSON

    response = requests.post(url, headers=headers, data=bad_json)

    assert response.status_code in (400, 500), ResponseAsserts._debug_response(response)


def test_create_booking_wrong_content_type_returns_error():
    url = f"{BASE_URL}/booking"
    payload = valid_booking_payload()

    # отправляем корректный JSON как строку, но Content-Type неправильный
    headers = {"Content-Type": "text/plain"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    assert response.status_code in (400, 415, 500), ResponseAsserts._debug_response(response)


def test_get_booking_not_existing_id_returns_404(rb_api):
    response = rb_api.get_booking(99999999)
    ResponseAsserts.assert_status(response, 404)