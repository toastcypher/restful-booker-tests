from datetime import datetime
from typing import Any, Dict, Optional

from jsonschema import validate, ValidationError


BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "number"},
        "booking": {
            "type": "object",
            "properties": {
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "number"},
                "depositpaid": {"type": "boolean"},
                "bookingdates": {
                    "type": "object",
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"},
                    },
                    "required": ["checkin", "checkout"],
                    "additionalProperties": True,
                },
                "additionalneeds": {"type": "string"},
            },
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
            "additionalProperties": True,
        },
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": True,
}


BOOKING_OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
            "required": ["checkin", "checkout"],
            "additionalProperties": True,
        },
        "additionalneeds": {"type": "string"},
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "additionalProperties": True,
}


class BookingAsserts:
    @staticmethod
    def _schema_fail_message(e: ValidationError, data: Any) -> str:
        path = "/".join(str(x) for x in e.path) if e.path else "<root>"
        schema_path = "/".join(str(x) for x in e.schema_path) if e.schema_path else "<schema>"
        return (
            "Schema validation failed.\n"
            f"Message: {e.message}\n"
            f"Data path: {path}\n"
            f"Schema path: {schema_path}\n"
            f"Data: {data}"
        )

    @staticmethod
    def assert_booking_response_schema(data: Any) -> None:
        try:
            validate(instance=data, schema=BOOKING_RESPONSE_SCHEMA)
        except ValidationError as e:
            raise AssertionError(BookingAsserts._schema_fail_message(e, data))

    @staticmethod
    def assert_booking_object_schema(data: Any) -> None:
        try:
            validate(instance=data, schema=BOOKING_OBJECT_SCHEMA)
        except ValidationError as e:
            raise AssertionError(BookingAsserts._schema_fail_message(e, data))

    @staticmethod
    def assert_date_format(date_str: Any, field_name: str = "date") -> None:
        assert isinstance(date_str, str), (
            f"{field_name} must be str. Got: {type(date_str)} value={date_str}"
        )
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise AssertionError(
                f"Invalid date format for {field_name}: {date_str}. Expected YYYY-MM-DD"
            )

    @staticmethod
    def assert_booking_dates_format(booking_obj: Dict[str, Any]) -> None:
        assert isinstance(booking_obj, dict), f"booking_obj must be dict. Got: {type(booking_obj)}"
        assert "bookingdates" in booking_obj, f"bookingdates missing. Got: {booking_obj}"

        bookingdates = booking_obj.get("bookingdates")
        assert isinstance(bookingdates, dict), f"bookingdates must be dict. Got: {type(bookingdates)} value={bookingdates}"

        checkin = bookingdates.get("checkin")
        checkout = bookingdates.get("checkout")

        assert checkin is not None, f"checkin missing in bookingdates. Got: {bookingdates}"
        assert checkout is not None, f"checkout missing in bookingdates. Got: {bookingdates}"

        BookingAsserts.assert_date_format(checkin, "checkin")
        BookingAsserts.assert_date_format(checkout, "checkout")

    @staticmethod
    def assert_booking_equals_subset(actual: Dict[str, Any], expected_subset: Dict[str, Any], context: Optional[str] = None) -> None:
        assert isinstance(actual, dict), f"actual must be dict. Got: {type(actual)} value={actual}"
        assert isinstance(expected_subset, dict), f"expected_subset must be dict. Got: {type(expected_subset)} value={expected_subset}"

        for key, expected_value in expected_subset.items():
            actual_value = actual.get(key)
            assert actual_value == expected_value, (
                    (f"{context}\n" if context else "")
                    + f"Field mismatch: {key}\n"
                      f"Expected: {expected_value}\n"
                      f"Actual: {actual_value}\n"
                      f"Actual object: {actual}"
            )