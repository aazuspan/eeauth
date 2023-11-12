import ee

from .api import (
    activate_user,
    authenticate,
    get_default_user,
    get_initialized_user,
    initialize,
    list_users,
    remove_user,
    reset,
)
from .exceptions import (
    NotAuthenticatedError,
    NotInitializedError,
    UnknownUserError,
    UserNotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    "activate_user",
    "list_users",
    "remove_user",
    "get_initialized_user",
    "get_default_user",
    "reset",
    "NotInitializedError",
    "NotAuthenticatedError",
    "UserNotFoundError",
    "UnknownUserError",
]


for fn, wrapper in zip((ee.Authenticate, ee.Initialize), (authenticate, initialize)):
    if not hasattr(fn, "as_user"):
        fn.as_user = wrapper
