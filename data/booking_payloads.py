import os
from typing import Dict, Any
from datetime import date, timedelta
import random
import string


def _random_string(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def valid_auth_credentials() -> Dict[str, str]:
    username = os.getenv("AUTH_USERNAME")
    password = os.getenv("AUTH_PASSWORD")

    if not username or not password:
        raise ValueError("AUTH_USERNAME or AUTH_PASSWORD not set in environment")

    return {
        "username": username,
        "password": password,
    }


def valid_booking_payload() -> Dict[str, Any]:
    today = date.today()
    return {
        "firstname": _random_string(),
        "lastname": _random_string(),
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": str(today),
            "checkout": str(today + timedelta(days=5)),
        },
        "additionalneeds": "Breakfast",
    }

def eq_totalprice() -> Dict[str, Any]:
    return {
        "valid_positive_int": 100,
        "invalid_negative": -1,
        "invalid_string": "abc",
        "invalid_null": None,
    }


def eq_depositpaid() -> Dict[str, Any]:
    return {
        "valid_true": True,
        "valid_false": False,
        "invalid_string": "true",
        "invalid_int": 1,
        "invalid_null": None,
    }


def eq_checkin_dates() -> Dict[str, Any]:
    return {
        "valid_format": "2025-01-10",
        "invalid_format_ddmmyyyy": "10-01-2025",
        "invalid_no_dashes": "20250110",
        "invalid_empty": "",
        "invalid_null": None,
    }

def booking_payload_with_totalprice(value: Any) -> Dict[str, Any]:
    payload = valid_booking_payload()
    payload["totalprice"] = value
    return payload


def booking_payload_with_depositpaid(value: Any) -> Dict[str, Any]:
    payload = valid_booking_payload()
    payload["depositpaid"] = value
    return payload


def booking_payload_with_checkin(value: Any) -> Dict[str, Any]:
    payload = valid_booking_payload()
    payload["bookingdates"]["checkin"] = value
    return payload


def booking_payload_missing_field(field_name: str) -> Dict[str, Any]:
    payload = valid_booking_payload()
    payload.pop(field_name, None)
    return payload