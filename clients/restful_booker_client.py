from typing import Optional, Dict, Any
import requests

class RestfulBookerClient:
    def __init__(self, api):
        self.api = api

    def ping(self) -> requests.Response:
        return self.api.request("GET", "/ping")

    def auth(self, username: str, password: str) -> requests.Response:
        if not isinstance(username, str):
            raise TypeError("username must be str")
        if not isinstance(password, str):
            raise TypeError("password must be str")
        payload: Dict[str, Any] = {"username": username, "password": password}
        return self.api.request("POST", "/auth", json=payload)

    def get_booking_ids(
            self,
            firstname: Optional[str] = None,
            lastname: Optional[str] = None,
            checkin: Optional[str] = None,
            checkout: Optional[str] = None,
    ) -> requests.Response:
        if firstname is not None and not isinstance(firstname, str):
            raise TypeError("firstname must be str")
        if lastname is not None and not isinstance(lastname, str):
            raise TypeError("lastname must be str")
        if checkin is not None:
            self._validate_date_str(checkin, "checkin")
        if checkout is not None:
            self._validate_date_str(checkout, "checkout")

        params: Dict[str, Any] = {}
        if firstname is not None:
            params["firstname"] = firstname
        if lastname is not None:
            params["lastname"] = lastname
        if checkin is not None:
            params["checkin"] = checkin
        if checkout is not None:
            params["checkout"] = checkout

        return self.api.request("GET", "/booking", params=params)

    def get_booking(self, booking_id: int) -> requests.Response:
        self._validate_booking_id(booking_id)
        return self.api.request("GET", f"/booking/{booking_id}")

    def create_booking(self, payload: Dict[str, Any]) -> requests.Response:
        if not isinstance(payload, dict):
            raise TypeError("payload must be dict")
        return self.api.request("POST", "/booking", json=payload)

    def update_booking_put(self, booking_id: int, payload: Dict[str, Any]) -> requests.Response:
        self._validate_booking_id(booking_id)
        if not isinstance(payload, dict):
            raise TypeError("payload must be dict")
        return self.api.request("PUT", f"/booking/{booking_id}", json=payload)

    def update_booking_patch(self, booking_id: int, payload: Dict[str, Any]) -> requests.Response:
        self._validate_booking_id(booking_id)
        if not isinstance(payload, dict):
            raise TypeError("payload must be dict")
        return self.api.request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id: int) -> requests.Response:
        self._validate_booking_id(booking_id)
        return self.api.request("DELETE", f"/booking/{booking_id}")

    @staticmethod
    def _validate_booking_id(booking_id: int) -> None:
        if not isinstance(booking_id, int):
            raise TypeError("booking_id must be int")

    @staticmethod
    def _validate_date_str(value: str, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be str")
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError(f"{field_name} must be in YYYY-MM-DD format")