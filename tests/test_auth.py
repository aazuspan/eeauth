import json

import pytest

import eeauth
from eeauth.errors import UserNotFoundError


@pytest.fixture()
def credential_path(tmpdir):
    from eeauth.registry import REGISTRY_PATH

    tmp_credentials = {
        "user1": {
            "refresh_token": "1//1234",
        },
        "user2": {
            "refresh_token": "1//5678",
        },
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(tmp_credentials, f)

    return REGISTRY_PATH


def test_list_users(credential_path):
    with open(credential_path) as f:
        print(json.load(f))

    assert eeauth.list_users() == ["user1", "user2"]


def test_reset(credential_path):
    eeauth.reset()

    with open(credential_path) as f:
        assert json.load(f) == {}


def test_remove_user(credential_path):
    eeauth.remove_user("user1")
    assert eeauth.list_users() == ["user2"]

    with pytest.raises(UserNotFoundError):
        eeauth.remove_user("user1")
