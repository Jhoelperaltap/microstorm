import pytest
from fastapi import FastAPI
from strictaccess import strict_access_control, public, private, protected

@strict_access_control()
class DummyRouter:
    def __init__(self):
        self._debug_mode = False  # Acceso restringido

    @public
    def allowed(self):
        return "ok"

    @protected
    def internal_method(self):
        return "should not be directly accessible"

    @private
    def secret_method(self):
        return "definitely not accessible"

def test_public_method():
    r = DummyRouter()
    assert r.allowed() == "ok"

def test_protected_access_violation():
    r = DummyRouter()
    with pytest.raises(Exception) as exc_info:
        r.internal_method()
    assert "protected" in str(exc_info.value).lower()

def test_private_access_violation():
    r = DummyRouter()
    with pytest.raises(Exception) as exc_info:
        r.secret_method()
    assert "private" in str(exc_info.value).lower()