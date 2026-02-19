import pytest

from config import BASE_URL
from clients.base_api_client import BaseApiClient
from clients.restful_booker_client import RestfulBookerClient
from data.booking_payloads import valid_auth_credentials, valid_booking_payload

@pytest.fixture
def api():
    return BaseApiClient(BASE_URL)

@pytest.fixture
def rb(api):
    return RestfulBookerClient(api)

@pytest.fixture
def auth_client(api, rb):
    creds = valid_auth_credentials()
    response = rb.auth(creds["username"], creds["password"])
    token = response.json()["token"]
    api.set_token(token)
    return rb

@pytest.fixture
def booking_factory(rb):
    created_ids = []

    def _create(payload=None):
        if payload is None:
            payload = valid_booking_payload()
        response = rb.create_booking(payload)
        booking_id = response.json()["bookingid"]
        created_ids.append(booking_id)
        return booking_id, payload

    return _create