import rich_click as click
from rich import print
from rich.prompt import Confirm
from rich.table import Table

from .auth import (
    _authenticate,
    activate_user,
    get_default_user,
    list_users,
    remove_user,
)
from .errors import UnknownUserError, UserNotFoundError
from .registry import open_user_registry


@click.group()
@click.version_option()
def cli():
    print("")


@cli.command()
@click.argument("user")
@click.option(
    "--auth-mode", "-m", default="notebook", help="The authentication mode to use."
)
def authenticate(user, auth_mode):
    """Authenticate USER and store their credentials."""
    if user in list_users() and not Confirm.ask(
        f"User [bold cyan]{user}[/] is already authenticated. Overwrite credentials?",
        default=False,
    ):
        print("")
        return

    _authenticate(user, auth_mode)
    print(
        f"\nAuthenticated [bold cyan]{user}[/]! "
        "Run `eeauth activate --user {user}` to set a new default user.\n"
    )


@cli.command()
@click.argument("user")
def activate(user):
    """Set USER as the default Earth Engine user."""
    try:
        activate_user(user)
        print(f"Activated [bold cyan]{user}[/] as the default Earth Engine user.\n")
    except UserNotFoundError:
        print(
            f"User [bold cyan]{user}[/] not found in the registry. "
            "Run `eeauth list` to see all authenticated users. "
            f"Run `eeauth authenticate --user {user}` to add a new user.\n"
        )


@cli.command(name="list")
def list_command():
    """List all authenticated users."""
    table = Table(
        title=f"Authenticated Users ({len(list_users())})",
        caption="*default user",
        expand=True,
        min_width=60,
    )
    table.add_column("User")
    table.add_column("Created", justify="right", style="dim")

    try:
        default_user = get_default_user()
    except UnknownUserError:
        default_user = None

    with open_user_registry() as reg:
        for user, creds in reg.items():
            row_style = None
            if user == default_user:
                user += "*"
                row_style = "bold cyan"
            table.add_row(user, creds["date_created"], style=row_style)

    print(table)
    print("")


@cli.command()
@click.argument("user")
def remove(user):
    """Remove USER from the registry."""
    try:
        default_user = get_default_user()
    except UnknownUserError:
        default_user = None

    if user == default_user and not Confirm.ask(
        f"[bold cyan]{user}[/] is the default user. "
        "Are you sure you want to remove it?",
        default=False,
    ):
        print("")
        return

    print("")
    try:
        remove_user(user)
        print(
            f"Removed [bold cyan]{user}[/] from the registry. "
            "The associated credentials have been forgotten.\n"
        )
    except UserNotFoundError:
        print(
            f"User [bold cyan]{user}[/] not found in the registry. "
            "Run `eeauth list` to see all authenticated users.\n"
        )
