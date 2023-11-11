import ee
import pytest

import eeauth


def test_builds_missing_registry(missing_registry):
    """Test that the registry is built if it doesn't exist."""
    assert eeauth.list_users() == []


def test_activate(registry):
    """Test that activating a user sets the default user."""
    eeauth.activate_user("extra_user")
    default_user = eeauth.get_default_user()
    assert default_user.name == "extra_user"

    # Reset to default
    eeauth.activate_user("default_user")
    default_user = eeauth.get_default_user()
    assert default_user.name == "default_user"


def test_get_initialized_user(registry):
    """Test that the initialized user is returned."""
    with pytest.raises(eeauth.NotInitializedError):
        eeauth.get_initialized_user()

    ee.Initialize()
    initialized_user = eeauth.get_initialized_user()
    assert initialized_user.name == "default_user"


def test_initialize_as_user(registry):
    """Test that ee.Initialize.as_user sets the requested user."""
    # ee.Initialize is mocked, so we need to call the wrapper directly
    eeauth.initialize("extra_user")
    assert eeauth.get_initialized_user().name == "extra_user"

    eeauth.initialize("default_user")
    assert eeauth.get_initialized_user().name == "default_user"


def test_list_users(registry):
    """Test that the registry is read and users are returned."""
    users = eeauth.list_users()
    user_names = [user.name for user in users]

    assert len(users) == 2
    assert user_names == ["default_user", "extra_user"]


def test_remove_user(registry):
    """Test that a user is removed from the registry."""
    user = eeauth.list_users()[1]

    eeauth.remove_user(user.name)
    users = eeauth.list_users()
    assert len(users) == 1
    assert user.name not in [user.name for user in users]


def test_authenticate(registry):
    """Test that a user is added to the registry when authenticated."""
    eeauth.authenticate("test_user3")

    users = eeauth.list_users()
    assert len(users) == 3
    assert "test_user3" in [user.name for user in users]


def test_reset(registry):
    """Test that the registry is reset to an empty state."""
    eeauth.reset()
    assert len(eeauth.list_users()) == 0


@pytest.mark.parametrize(
    "check_method", [eeauth.activate_user, eeauth.remove_user, eeauth.initialize]
)
def test_usernotfound(check_method, registry):
    """Test that UserNotFoundError is raised when a user is not found."""
    with pytest.raises(eeauth.UserNotFoundError):
        check_method("non_existent_user")


@pytest.mark.parametrize(
    "check_method", [eeauth.get_default_user, eeauth.get_initialized_user]
)
def test_unknownuser(check_method, registry):
    """Test for UnknownUserError when the default/initialized user is missing."""
    ee.Initialize()
    user_to_remove = check_method()
    eeauth.remove_user(user_to_remove.name)
    with pytest.raises(eeauth.UnknownUserError):
        check_method()
