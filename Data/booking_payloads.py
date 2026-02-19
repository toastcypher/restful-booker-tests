def valid_auth_credentials():
    return {
        "username": "admin",
        "password": "password123"
    }

def invalid_auth_credentials():
    return {
        "username": "admin",
        "password": "wrong_password"
    }

def valid_booking_payload():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-10"
        },
        "additionalneeds": "Breakfast"
    }

def invalid_booking_missing_lastname():
    payload = valid_booking_payload().copy()
    payload.pop("lastname")
    return payload

def invalid_booking_bad_dates():
    payload = valid_booking_payload().copy()
    payload["bookingdates"]["checkin"] = "invalid-date"
    return payload