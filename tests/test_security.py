import pytest
from microstorm.security import security

def test_generate_and_verify_token():
    payload = {"user_id": "123"}
    token = security.generate_token(payload)
    decoded = security.verify_token(token)
    assert decoded["user_id"] == "123"

def test_invalid_token_raises():
    with pytest.raises(Exception):
        security.verify_token("invalid.token")