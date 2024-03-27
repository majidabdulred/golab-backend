import pytest
from mongomock_motor import AsyncMongoMockClient
from starlette.testclient import TestClient
from app import db_client
from pytest_assume.plugin import assume


def get_fake_client():
    fake_client = AsyncMongoMockClient()
    print("FAKE CLIENT")
    return fake_client


db_client.get_db_client = get_fake_client

from main import app


@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch):
    monkeypatch.setattr("app.send_mail.smtp_send_mail", lambda msg: None)
    monkeypatch.setattr("app.db.create_random_otp", lambda: 12345)


testclient = TestClient(app)


def test_is_on():
    response = testclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Good to go Chief!"}


def test_signup():
    response = testclient.post(
        "/auth/signup",
        json={"name": "Abdul Majid", "email": "majid@metex.co", "password": "password"},
    )
    with assume:
        assert response.status_code == 200
    with assume:
        assert response.json().get("otp_id") is not None

    otp_id = response.json().get("otp_id")
    response = testclient.post(
        "/auth/verify_otp", json={"otp_id": otp_id, "otp": 12345}
    )
    with assume:
        assert response.status_code == 200
    with assume:
        assert response.json() == {"verified": True}


def test_login():
    response = testclient.post(
        "/auth/token", data={"username": "majid@metex.co", "password": "password"}
    )
    with assume:
        assert response.status_code == 200
    with assume:
        assert response.json().get("access_token") is not None


def test_forgot_password():
    response = testclient.post("/auth/reset/send_otp", json={"email": "majid@metex.co"})
    with assume:
        assert response.status_code == 200
    with assume:
        assert response.json().get("otp_id") is not None

    otp_id = response.json().get("otp_id")
    response = testclient.post(
        "/auth/reset/verify_otp", json={"otp_id": otp_id, "otp": 12345}
    )
    with assume:
        assert response.status_code == 200
    with assume:
        assert response.json() == {"verified": True}
