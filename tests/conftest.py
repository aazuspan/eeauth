import json
from pathlib import Path
from unittest.mock import patch

import ee
import pytest

from eeauth import user_registry

DEFAULT_CREDENTIALS = {
    "refresh_token": "1//refresh-token-1",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "client-id.apps.googleusercontent.com",
    "client_secret": "client-secret",
    "scopes": [
        "https://www.googleapis.com/auth/earthengine",
        "https://www.googleapis.com/auth/devstorage.full_control",
    ],
}

EXTRA_CREDENTIALS = DEFAULT_CREDENTIALS.copy()
EXTRA_CREDENTIALS["refresh_token"] = "1//refresh-token-2"

MOCK_REGISTRY = {
    "default_user": {
        "name": "default_user",
        "credentials": DEFAULT_CREDENTIALS,
        "date_created": "2022-01-01",
    },
    "extra_user": {
        "name": "extra_user",
        "credentials": EXTRA_CREDENTIALS,
        "date_created": "1954-01-01",
    },
}


@pytest.fixture(autouse=True)
def registry(tmpdir, request):
    """Build a test registry at a temporary path and point eeauth to it.

    Each test invocation will get a new registry. Tests marked with "missing_registry"
    will get a registry path that doesn't exist.
    """
    path = tmpdir.join("test_reg.json")

    if "missing_registry" not in request.keywords:
        with open(path, "w") as f:
            json.dump(MOCK_REGISTRY, f)

    with patch("eeauth.user_registry.get_registry_path") as mock:
        mock.return_value = Path(path)
        yield mock


@pytest.fixture(autouse=True)
def persistent_credentials(tmpdir, request):
    """Build persistent credentials at a temporary path and point EE to it.

    Each test invocation will get a new set of credentials. Tests marked with
    "missing_credentials" will get a credentials path that doesn't exist.
    """
    path = tmpdir.join("credentials")

    if "missing_credentials" not in request.keywords:
        with open(path, "w") as f:
            json.dump(DEFAULT_CREDENTIALS, f)

    with patch("ee.oauth.get_credentials_path") as mock:
        mock.return_value = str(path)
        yield mock


@pytest.fixture(scope="session", autouse=True)
def mock_ee_authenticate():
    """Mock ee.Authenticate to write fake persistent credentials."""
    with patch("ee.Authenticate") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_ee_initialize():
    """Mock ee.Initialize to set internal credentials."""

    def set_credentials(credentials=None):
        """Credentials may be passed directly when initialized by eeauth."""
        if credentials is None:
            credentials = (
                user_registry.Credentials.from_persistent_credentials().to_oauth()
            )

        ee.data._credentials = credentials

    with patch("ee.Initialize") as mock:
        mock.side_effect = set_credentials
        yield mock

    ee.data._credentials = None


def _get_json_contents_or_none(path):
    """Return the contents of a file or None if it doesn't exist."""
    if not Path(path).exists():
        return None

    with open(path) as f:
        return json.load(f)


@pytest.fixture(autouse=True)
def _check_persistent_credentials_unchanged(request):
    """Check to make sure persistent EE credentials were not affected by tests."""
    # Setup
    path = ee.oauth.get_credentials_path()
    init_credentials = _get_json_contents_or_none(path)

    yield

    # Teardown
    path = ee.oauth.get_credentials_path()
    credentials = _get_json_contents_or_none(path)

    assert credentials == init_credentials


@pytest.fixture(autouse=True)
def _check_registry_unchanged(request):
    """Check to make sure the eeauth registry was not affected by tests."""
    # Setup
    path = user_registry.get_registry_path()
    init_registry = _get_json_contents_or_none(path)

    yield

    # Teardown
    path = user_registry.get_registry_path()
    registry = _get_json_contents_or_none(path)

    assert registry == init_registry
