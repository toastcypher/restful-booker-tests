import pytest
from asserts.response_asserts import ResponseAsserts
from asserts.booking_asserts import BookingAsserts
from data.booking_payloads import (
    valid_booking_payload,
    eq_totalprice,
    eq_depositpaid,
    booking_payload_with_totalprice,
    booking_payload_with_depositpaid,
)

def test_create_booking_success(auth_rb_api):
    payload = valid_booking_payload()

    response = auth_rb_api.create_booking(payload)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    ResponseAsserts.assert_json_has_keys(data, ["bookingid", "booking"])

    BookingAsserts.assert_booking_response_schema(data)
    booking = data["booking"]
    BookingAsserts.assert_booking_dates_format(booking)
    BookingAsserts.assert_booking_equals_subset(booking, payload)


def test_get_booking_by_id_success(auth_rb_api, booking_factory):
    booking_id, payload = booking_factory()

    response = auth_rb_api.get_booking(booking_id)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    booking = ResponseAsserts.parse_json(response)
    BookingAsserts.assert_booking_object_schema(booking)
    BookingAsserts.assert_booking_dates_format(booking)
    BookingAsserts.assert_booking_equals_subset(booking, payload)


def test_update_booking_put_success(auth_rb_api, booking_factory):
    booking_id, _ = booking_factory()
    new_payload = valid_booking_payload()

    response = auth_rb_api.update_booking_put(booking_id, new_payload)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    booking = ResponseAsserts.parse_json(response)
    BookingAsserts.assert_booking_object_schema(booking)
    BookingAsserts.assert_booking_dates_format(booking)
    BookingAsserts.assert_booking_equals_subset(booking, new_payload)


def test_update_booking_patch_success(auth_rb_api, booking_factory):
    booking_id, original_payload = booking_factory()
    patch_payload = {"firstname": "PatchedName"}

    response = auth_rb_api.update_booking_patch(booking_id, patch_payload)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    booking = ResponseAsserts.parse_json(response)
    BookingAsserts.assert_booking_object_schema(booking)
    BookingAsserts.assert_booking_dates_format(booking)
    assert booking["firstname"] == patch_payload["firstname"]
    assert booking["lastname"] == original_payload["lastname"]

def test_delete_booking_success(auth_rb_api, booking_factory):
    booking_id, _ = booking_factory()

    response = auth_rb_api.delete_booking(booking_id)
    ResponseAsserts.assert_status(response, 201)

    response_get = auth_rb_api.get_booking(booking_id)
    ResponseAsserts.assert_status(response_get, 404)

@pytest.mark.parametrize(
    "label,value",
    [(k, v) for k, v in eq_totalprice().items() if k.startswith("valid_")],
)
def test_create_booking_totalprice_equivalence_classes(auth_rb_api, label, value):
    payload = booking_payload_with_totalprice(value)

    response = auth_rb_api.create_booking(payload)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    booking = data["booking"]

    BookingAsserts.assert_booking_dates_format(booking)
    BookingAsserts.assert_booking_equals_subset(booking, payload, context=f"totalprice class={label}")


@pytest.mark.parametrize(
    "label,value",
    [(k, v) for k, v in eq_depositpaid().items() if k.startswith("valid_")],
)
def test_create_booking_depositpaid_equivalence_classes(auth_rb_api, label, value):
    payload = booking_payload_with_depositpaid(value)

    response = auth_rb_api.create_booking(payload)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = ResponseAsserts.parse_json(response)
    booking = data["booking"]

    BookingAsserts.assert_booking_dates_format(booking)
    BookingAsserts.assert_booking_equals_subset(booking, payload, context=f"depositpaid class={label}")