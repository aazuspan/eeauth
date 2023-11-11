import click

from .api import (
    activate_user,
    authenticate,
    get_default_user,
    list_users,
    remove_user,
)
from .exceptions import UnknownUserError, UserNotFoundError
from .user_registry import UserRegistry


@click.group()
@click.version_option()
def cli():
    """Manage Earth Engine authentication."""
    click.echo("")


@cli.command(name="authenticate")
@click.argument("user")
@click.option(
    "--auth-mode", "-m", default="notebook", help="The authentication mode to use."
)
def authenticate_command(user: str, auth_mode: str):
    """Authenticate USER and store their credentials."""
    if user in (user.name for user in list_users()):
        msg = f"User `{user}` is already authenticated. Overwrite credentials? [y/N] "
        if input(msg).lower() != "y":
            click.echo("Cancelling.\n")
            return

    authenticate(user, auth_mode)
    click.echo(f"\nAuthenticated `{user}`!\n")
    click.echo(f"* Run `eeauth activate {user}` to set a new default user.\n")


@cli.command()
@click.argument("user")
def activate(user: str):
    """Set USER as the default Earth Engine user."""
    try:
        activate_user(user)
        click.echo(f"Activated `{user}` as the default Earth Engine user.\n")
    except UserNotFoundError:
        click.echo(f"User `{user}` not found in the registry.\n")
        click.echo("* Run `eeauth list` to see all authenticated users.")
        click.echo(f"* Run `eeauth authenticate {user}` to add a new user.\n")


@cli.command(name="list")
def list_command():
    """List all authenticated users."""
    click.echo(f"{'Name':<20}{'Created':>36}")
    click.echo("-" * 56)

    registry = UserRegistry.open()
    for user in registry.users.values():
        star = "*" if _is_default_user(user.name) else ""
        click.echo(f"{user.name + star:<20}{user.date_created:>36}")
    click.echo("")


@cli.command()
@click.argument("user")
def remove(user: str):
    """Remove USER from the registry."""
    try:
        remove_user(user)
        click.echo(f"Removed user `{user}` from the registry.\n")
    except UserNotFoundError:
        click.echo(f"User `{user}` not found in the registry.\n")
        click.echo("* Run `eeauth list` to see all authenticated users.\n")


def _is_default_user(name: str) -> bool:
    """Check if a user's name matches the default user."""
    try:
        return get_default_user().name == name
    except UnknownUserError:
        return False
