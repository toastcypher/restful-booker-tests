from asserts.response_asserts import ResponseAsserts


def test_get_booking_ids_no_filters_returns_list(rb_api):
    response = rb_api.get_booking_ids()
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    try:
        data = response.json()
    except ValueError:
        raise AssertionError(ResponseAsserts._debug_response(response))

    assert isinstance(data, list), f"Expected list, got {type(data)}. Data: {data}"
    if data:
        assert "bookingid" in data[0], f"Expected bookingid field. Data: {data[0]}"


def test_get_booking_ids_filter_by_name_returns_list(rb_api, booking_factory):
    booking_id, payload = booking_factory()

    response = rb_api.get_booking_ids(firstname=payload["firstname"], lastname=payload["lastname"])
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}. Data: {data}"

    ids = [item.get("bookingid") for item in data if isinstance(item, dict)]
    assert booking_id in ids, f"Created booking_id {booking_id} not found in filtered results. Got: {ids}"


def test_get_booking_ids_filter_by_dates_returns_list(rb_api, booking_factory):
    _, payload = booking_factory()
    checkin = payload["bookingdates"]["checkin"]
    checkout = payload["bookingdates"]["checkout"]

    response = rb_api.get_booking_ids(checkin=checkin, checkout=checkout)
    ResponseAsserts.assert_status(response, 200)
    ResponseAsserts.assert_content_type_contains(response, "application/json")

    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}. Data: {data}"

    for item in data[:5]:
        assert isinstance(item, dict), f"Expected dict item, got {type(item)}. Item: {item}"
        assert "bookingid" in item, f"Missing bookingid in item: {item}"