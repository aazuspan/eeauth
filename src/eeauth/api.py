import json

import ee

from .exceptions import NotInitializedError
from .user_registry import Credentials, User, UserRegistry


def reset() -> None:
    """
    Reset the registry to an empty state.
    """
    with UserRegistry.open() as registry:
        registry.users.clear()


def list_users() -> list[User]:
    """
    List the users in the registry.
    """
    registry = UserRegistry.open()
    return list(registry.users.values())


def remove_user(name: str) -> None:
    """
    Remove a user from the registry.
    """
    with UserRegistry.open() as registry:
        registry.remove_user(name)


def activate_user(name: str) -> None:
    """
    Set a user as the default user for `ee.Initialize`.
    """
    registry = UserRegistry.open()
    user = registry.get_user(name)

    with open(ee.oauth.get_credentials_path(), "w") as f:
        json.dump(user.credentials.model_dump(), f, indent=2)


def get_initialized_user() -> User:
    """
    Get the currently initialized user.
    """
    credentials = ee.data._credentials
    if credentials is None:
        raise NotInitializedError("Earth Engine is not initialized.")

    registry = UserRegistry.open()
    return registry.find_user(refresh_token=credentials.refresh_token)


def get_default_user() -> User:
    """
    Get the user in the persistent credentials.
    """
    credentials = Credentials.from_persistent_credentials()
    registry = UserRegistry.open()
    return registry.find_user(refresh_token=credentials.refresh_token)


def initialize(name: str, **kwargs) -> None:
    """
    Initialize Earth Engine using the credentials of the registered user.
    """
    registry = UserRegistry.open()
    user = registry.get_user(name)
    credentials = user.credentials.to_oauth()
    ee.Initialize(credentials=credentials, **kwargs)


def authenticate(name: str, auth_mode: str = "notebook", **kwargs) -> None:
    """
    Authenticate Earth Engine and store the credentials for the registered user.

    Parameters
    ----------
    name : str
        The name of the user to authenticate. This name is used locally, and does not
        need to match the associated Google account.
    """
    ee.Authenticate(auth_mode=auth_mode, **kwargs)
    user = User.from_persistent_credentials(name=name)

    with UserRegistry.open() as registry:
        registry.add_user(user)
