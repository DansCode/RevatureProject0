from utilities import dbUtil
import pytest


@pytest.mark.parametrize("usr, pwd, expected", (
    ("banana", "fish", True), (" ", "a", None), (".....", "b", None)
))
def test_auth(usr, pwd, expected):
    assert dbUtil.authenticate(usr, pwd) is expected
