from datetime import datetime
from typing import Any, Dict


class BookingAsserts:

    @staticmethod
    def assert_date_format(date_str: str, field_name: str = "date") -> None:
        assert isinstance(date_str, str), f"{field_name} must be str. Got: {type(date_str)} value={date_str}"
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise AssertionError(f"Invalid date format for {field_name}: {date_str}. Expected YYYY-MM-DD")

    @staticmethod
    def assert_booking_has_required_fields(data: Dict[str, Any]) -> None:
        required = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
        missing = [k for k in required if k not in data]
        assert not missing, f"Missing booking fields: {missing}. Got: {data}"

        assert isinstance(data["bookingdates"], dict), f"bookingdates is not an object. Got: {data}"

        date_missing = [k for k in ["checkin", "checkout"] if k not in data["bookingdates"]]
        assert not date_missing, f"Missing bookingdates fields: {date_missing}. Got: {data}"

    @staticmethod
    def assert_booking_equals_subset(actual: Dict[str, Any], expected_subset: Dict[str, Any]) -> None:
        for key, value in expected_subset.items():
            assert actual.get(key) == value, f"Mismatch for {key}: expected {value}, got {actual.get(key)}"

    @staticmethod
    def assert_booking_dates_format(booking: Dict[str, Any]) -> None:
        BookingAsserts.assert_booking_has_required_fields(booking)
        checkin = booking["bookingdates"]["checkin"]
        checkout = booking["bookingdates"]["checkout"]

        BookingAsserts.assert_date_format(checkin, "checkin")
        BookingAsserts.assert_date_format(checkout, "checkout")