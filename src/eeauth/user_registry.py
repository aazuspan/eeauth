from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Optional

import ee
from google.oauth2.credentials import Credentials as OAuthCredentials
from pydantic import BaseModel

from .exceptions import NotAuthenticatedError, UnknownUserError, UserNotFoundError


def get_registry_path() -> Path:
    return Path("~/.config/eeauth/registry.json").expanduser()


class Credentials(BaseModel):
    """Earth Engine credentials."""

    refresh_token: str
    token_uri: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    scopes: Optional[list[str]] = None

    def to_oauth(self) -> OAuthCredentials:
        """Convert to OAuth credentials."""
        return OAuthCredentials(
            token=None,
            refresh_token=self.refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes,
        )

    @classmethod
    def from_persistent_credentials(cls) -> Credentials:
        """Create credentials from the persistent Earth Engine credentials."""
        try:
            args = ee.oauth.get_credentials_arguments()
        except FileNotFoundError:
            raise NotAuthenticatedError() from None

        return cls(**args)


class User(BaseModel):
    """A user with Earth Engine credentials."""

    name: str
    credentials: Credentials
    date_created: str

    @classmethod
    def from_persistent_credentials(cls, *, name: str) -> User:
        """Create a user from the persistent Earth Engine credentials."""
        credentials = Credentials.from_persistent_credentials()
        created = datetime.now().isoformat()
        return cls(name=name, credentials=credentials, date_created=created)


class UserRegistry(BaseModel):
    """A JSON-backed registry of Earth Engine user credentials."""

    users: dict[str, User]
    path: Path

    def __enter__(self) -> UserRegistry:
        self._init_users = deepcopy(self.users)
        return self

    def __exit__(self, *_) -> None:
        if self.users != self._init_users:
            self.save()

    @classmethod
    def open(cls) -> UserRegistry:
        """Create a user registry from the default file."""
        path = get_registry_path()

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump({}, f)

        with open(path) as f:
            return cls(users=json.load(f), path=path)

    def save(self) -> None:
        """Save the user registry to a file."""
        with open(self.path, "w") as f:
            json.dump(self.model_dump()["users"], f, indent=2)

    def add_user(self, user: User) -> None:
        """Add a user to the registry."""
        self.users[user.name] = user

    def get_user(self, user: str) -> User:
        """Get a user from the registry."""
        try:
            return self.users[user]
        except KeyError:
            raise UserNotFoundError(user) from None

    def remove_user(self, user: str) -> None:
        """Remove a user from the registry."""
        try:
            del self.users[user]
        except KeyError:
            raise UserNotFoundError(user) from None

    def find_user(self, *, refresh_token: str) -> User:
        """Find a user by their credentials."""
        for user in self.users.values():
            if user.credentials.refresh_token == refresh_token:
                return user

        raise UnknownUserError()
