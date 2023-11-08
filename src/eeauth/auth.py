import json

import ee
from google.oauth2.credentials import Credentials

from .errors import NotInitializedError, UnknownUserError
from .registry import open_user_registry


def reset():
    """
    Reset the registry to an empty state.
    """
    with open_user_registry(read_only=False) as reg:
        reg.clear()


def list_users():
    """
    List the names of users in the registry.
    """
    with open_user_registry() as reg:
        return list(reg.keys())


def remove_user(user):
    """
    Remove a user from the registry.
    """
    with open_user_registry(read_only=False) as reg:
        del reg[user]


def activate_user(user):
    """
    Set a user as the default user for `ee.Initialize`.
    """
    with open_user_registry() as reg:
        credentials = reg[user]

    with open(ee.oauth.get_credentials_path(), "w") as f:
        json.dump(credentials, f)


def _get_credentials(user) -> Credentials:
    """
    Retrieve OAuth Credentials for the registered user.
    """
    with open_user_registry() as reg:
        return Credentials(None, **reg[user])


def get_initialized_user():
    """Get the name of the currently initialized user."""
    credentials = ee.data._credentials
    if credentials is None:
        raise NotInitializedError("Earth Engine is not initialized.")

    with open_user_registry() as reg:
        for user, creds in reg.items():
            if creds["refresh_token"] == credentials.refresh_token:
                return user

    raise UnknownUserError()


def _initialize(user, *args, **kwargs):
    """
    Initialize Earth Engine using the credentials of the registered user.
    """
    creds = _get_credentials(user)
    return ee.Initialize(creds, *args, **kwargs)


def _authenticate(user, auth_mode="notebook", **kwargs):
    """
    Authenticate Earth Engine and store the credentials for the registered user.

    Parameters
    ----------
    user : str
        The name of the user to authenticate. This name is used locally, and does not
        need to match the associated Google account.
    """
    ee.Authenticate(auth_mode=auth_mode, **kwargs)
    persistent_credentials = ee.oauth.get_credentials_arguments()

    with open_user_registry(read_only=False) as reg:
        reg[user] = persistent_credentials