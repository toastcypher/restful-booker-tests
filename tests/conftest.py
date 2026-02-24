import pytest

from config import BASE_URL
from clients.base_api_client import BaseApiClient
from clients.restful_booker_client import RestfulBookerClient
from data.booking_payloads import valid_auth_credentials, valid_booking_payload

@pytest.fixture
def base_api():
    return BaseApiClient(BASE_URL)

@pytest.fixture
def rb_api(base_api):
    return RestfulBookerClient(base_api)

@pytest.fixture
def auth_rb_api(base_api, rb_api):
    creds = valid_auth_credentials()
    response = rb_api.auth(creds["username"], creds["password"])
    token = response.json()["token"]
    base_api.set_token(token)
    return rb_api

@pytest.fixture
def booking_factory(auth_rb_api):
    created_ids = []

    def _create(payload=None):
        if payload is None:
            payload = valid_booking_payload()
        response = auth_rb_api.create_booking(payload)
        booking_id = response.json()["bookingid"]
        created_ids.append(booking_id)
        return booking_id, payload

    yield _create

    for booking_id in created_ids:
        auth_rb_api.delete_booking(booking_id)