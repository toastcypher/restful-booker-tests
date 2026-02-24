import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")

AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
if not AUTH_USERNAME or not AUTH_PASSWORD:
    raise ValueError("AUTH_USERNAME and AUTH_PASSWORD must be set in environment")