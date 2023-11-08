import ee

from .auth import (
    _authenticate,
    _initialize,
    activate_user,
    get_initialized_user,
    list_users,
    remove_user,
    reset,
)

__version__ = "0.1.0"

__all__ = [
    "activate_user",
    "list_users",
    "remove_user",
    "get_initialized_user",
    "reset",
]


for fn, wrapper in zip((ee.Authenticate, ee.Initialize), (_authenticate, _initialize)):
    if not hasattr(fn, "as_user"):
        fn.as_user = wrapper
