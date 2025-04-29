import pytest
from strictaccess import strict_access_control, public, private, AccessControlMixin

@strict_access_control()
class Example:
    def __init__(self):
        self._debug_mode = True

    @public
    def allowed(self):
        return "ok"

    @private
    def hidden(self):
        return "secret"

def test_public_method():
    obj = Example()
    assert obj.allowed() == "ok"

def test_private_method_blocked():
    obj = Example()
    obj._debug_mode = False
    with pytest.raises(Exception):
        obj.hidden()