class BookingAsserts:

    @staticmethod
    def assert_booking_has_required_fields(data):
        required = ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
        missing = [k for k in required if k not in data]
        assert not missing, f"Missing booking fields: {missing}. Got: {data}"

        assert isinstance(data["bookingdates"], dict), f"bookingdates is not an object. Got: {data}"

        date_missing = [k for k in ["checkin", "checkout"] if k not in data["bookingdates"]]
        assert not date_missing, f"Missing bookingdates fields: {date_missing}. Got: {data}"

    @staticmethod
    def assert_booking_equals_subset(actual, expected_subset):
        for key, value in expected_subset.items():
            assert actual.get(key) == value, f"Mismatch for {key}: expected {value}, got {actual.get(key)}"

    @staticmethod
    def assert_booking_dates_format(data):
        checkin = data["bookingdates"]["checkin"]
        checkout = data["bookingdates"]["checkout"]

        assert isinstance(checkin, str) and len(checkin) == 10 and checkin[4] == "-" and checkin[7] == "-", \
            f"Invalid checkin date format: {checkin}"
        assert isinstance(checkout, str) and len(checkout) == 10 and checkout[4] == "-" and checkout[7] == "-", \
            f"Invalid checkout date format: {checkout}"