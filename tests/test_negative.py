import json
import requests

from config import BASE_URL
from asserts.response_asserts import ResponseAsserts
from data.booking_payloads import valid_booking_payload


def test_update_booking_put_without_auth_returns_unauthorized(rb_api, booking_factory):
    booking_id, payload = booking_factory()

    response = rb_api.update_booking_put(booking_id, payload)
    assert response.status_code in (401, 403), ResponseAsserts.debug_response(response)


def test_update_booking_patch_without_auth_returns_unauthorized(rb_api, booking_factory):
    booking_id, _ = booking_factory()
    patch_payload = {"firstname": "NoAuthPatch"}

    response = rb_api.update_booking_patch(booking_id, patch_payload)
    assert response.status_code in (401, 403), ResponseAsserts.debug_response(response)


def test_delete_booking_without_auth_returns_unauthorized(rb_api, booking_factory):
    booking_id, _ = booking_factory()

    response = rb_api.delete_booking(booking_id)
    assert response.status_code in (401, 403), ResponseAsserts.debug_response(response)


def test_create_booking_invalid_json_returns_error():
    url = f"{BASE_URL}/booking"
    headers = {"Content-Type": "application/json"}
    bad_json = '{"firstname": "A", "lastname":'  # намеренно битый JSON

    response = requests.post(url, headers=headers, data=bad_json)

    assert response.status_code in (400, 500), ResponseAsserts.debug_response(response)


def test_create_booking_wrong_content_type_returns_error():
    url = f"{BASE_URL}/booking"
    payload = valid_booking_payload()

    # отправляем корректный JSON как строку, но Content-Type неправильный
    headers = {"Content-Type": "text/plain"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    assert response.status_code in (400, 415, 500), ResponseAsserts.debug_response(response)


def test_get_booking_not_existing_id_returns_404(rb_api):
    response = rb_api.get_booking(99999999)
    ResponseAsserts.assert_status(response, 404)