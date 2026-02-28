from datetime import datetime
from typing import Any, Dict
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
                        "checkout": {"type": "string"}
                    },
                    "required": ["checkin", "checkout"]
                },
                "additionalneeds": {"type": "string"}
            },
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates"
            ]
        }
    },
    "required": ["bookingid", "booking"]
}

class BookingAsserts:

    @staticmethod
    def assert_date_format(date_str: str, field_name: str = "date") -> None:
        assert isinstance(date_str, str), f"{field_name} must be str. Got: {type(date_str)} value={date_str}"
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise AssertionError(f"Invalid date format for {field_name}: {date_str}. Expected YYYY-MM-DD")

    @staticmethod
    def assert_booking_equals_subset(actual: Dict[str, Any], expected_subset: Dict[str, Any]) -> None:
        for key, value in expected_subset.items():
            assert actual.get(key) == value, f"Mismatch for {key}: expected {value}, got {actual.get(key)}"


    @staticmethod
    def assert_booking_schema(data):
        try:
            validate(instance=data, schema=BOOKING_RESPONSE_SCHEMA)
        except ValidationError as e:
            raise AssertionError(f"Schema validation failed: {e.message}")


        BookingAsserts.assert_date_format(checkin, "checkin")
        BookingAsserts.assert_date_format(checkout, "checkout")

