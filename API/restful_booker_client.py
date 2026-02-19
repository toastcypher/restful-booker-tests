class RestfulBookerClient:
    def __init__(self, api):
        self.api = api

    def ping(self):
        return self.api.request("GET", "/ping")

    def auth(self, username, password):
        payload = {"username": username, "password": password}
        return self.api.request("POST", "/auth", json=payload)

    def get_booking_ids(self, firstname=None, lastname=None, checkin=None, checkout=None):
        params = {}
        if firstname is not None:
            params["firstname"] = firstname
        if lastname is not None:
            params["lastname"] = lastname
        if checkin is not None:
            params["checkin"] = checkin
        if checkout is not None:
            params["checkout"] = checkout
        return self.api.request("GET", "/booking", params=params)

    def create_booking(self, payload):
        return self.api.request("POST", "/booking", json=payload)

    def get_booking(self, booking_id):
        return self.api.request("GET", f"/booking/{booking_id}")

    def update_booking_put(self, booking_id, payload):
        return self.api.request("PUT", f"/booking/{booking_id}", json=payload)

    def update_booking_patch(self, booking_id, payload):
        return self.api.request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id):
        return self.api.request("DELETE", f"/booking/{booking_id}")