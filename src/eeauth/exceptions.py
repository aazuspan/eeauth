class UserNotFoundError(ValueError):
    """No credentials are registered for a named user."""

    def __init__(self, user):
        msg = (
            f"No credentials registered for `{user}`. "
            f"Run `ee.Authenticate.as_user('{user}')` "
            "to store the appropriate credentials."
        )
        super().__init__(msg)


class UnknownUserError(ValueError):
    """The credentials of a user are not in the registry."""

    def __init__(self):
        msg = "No users are registered with those credentials."
        super().__init__(msg)


class NotInitializedError(ValueError):
    """Earth Engine has not been initialized."""

    def __init__(self):
        msg = (
            "Earth Engine is not initialized. "
            "Run `ee.Initialize()` or `ee.Initialize.as_user( ... )` to initialize."
        )
        super().__init__(msg)


class NotAuthenticatedError(ValueError):
    """Earth Engine has not been authenticated, so no persistent credentials exist."""

    def __init__(self):
        msg = (
            "No persistent credentials could be found. "
            "Run `ee.Authenticate()` or `ee.Authenticate.as_user( ... )` to "
            "authenticate an account."
        )
        super().__init__(msg)
