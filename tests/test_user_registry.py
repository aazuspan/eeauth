import json
from datetime import datetime

import pytest
from google.oauth2.credentials import Credentials as OAuthCredentials

from eeauth.exceptions import UnknownUserError, UserNotFoundError
from eeauth.user_registry import Credentials, User, UserRegistry


@pytest.fixture()
def credentials() -> Credentials:
    return Credentials(refresh_token="1234")


@pytest.fixture()
def user(credentials) -> User:
    return User(name="test_user", credentials=credentials, date_created="2022-01-01")


def test_add_user(tmpdir, user: User, credentials: Credentials):
    with UserRegistry.open(tmpdir.join("test_reg.json")) as registry:
        registry.add_user(user)

    assert registry.get_user("test_user") == user
    with open(registry.path) as f:
        assert json.load(f) == {
            "test_user": {
                "name": "test_user",
                "credentials": credentials.model_dump(),
                "date_created": "2022-01-01",
            }
        }


def test_get_user(tmpdir, user):
    with UserRegistry.open(tmpdir.join("test_reg.json")) as registry:
        registry.add_user(user)

    with pytest.raises(UserNotFoundError):
        registry.get_user("non_existent_user")


def test_remove_user(tmpdir, user):
    with UserRegistry.open(tmpdir.join("test_reg.json")) as registry:
        registry.add_user(user)

    registry.remove_user("test_user")
    with pytest.raises(UserNotFoundError):
        registry.remove_user("test_user")


def test_find_user(tmpdir, user):
    with UserRegistry.open(tmpdir.join("test_reg.json")) as registry:
        registry.add_user(user)

    assert registry.find_user(refresh_token="1234") == user

    with pytest.raises(UnknownUserError):
        registry.find_user(refresh_token="non_existent_token")


def test_credentials_to_oauth(credentials: Credentials):
    assert isinstance(credentials.to_oauth(), OAuthCredentials)


def test_credentials_from_persistent():
    # This requires that Earth Engine is authenticated on the local machine
    credentials = Credentials.from_persistent_credentials()
    assert isinstance(credentials, Credentials)


def test_user_from_persistent():
    # This requires that Earth Engine is authenticated on the local machine
    user = User.from_persistent_credentials(name="test_user")
    assert isinstance(user, User)
    assert user.name == "test_user"
    assert isinstance(user.credentials, Credentials)
    assert isinstance(datetime.fromisoformat(user.date_created), datetime)
