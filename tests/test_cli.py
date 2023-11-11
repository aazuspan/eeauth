import pytest
from click.testing import CliRunner

import eeauth.cli as cli


@pytest.fixture()
def runner():
    return CliRunner()


def test_activate(runner, registry):
    result = runner.invoke(cli.activate, ["extra_user"])
    assert result.exit_code == 0
    assert "Activated `extra_user`" in result.output


def test_remove(runner, registry):
    result = runner.invoke(cli.remove, ["extra_user"])
    assert result.exit_code == 0
    assert "Removed `extra_user`" in result.output


@pytest.mark.parametrize("check_command", [cli.activate, cli.remove])
def test_user_not_found(check_command, runner, registry):
    result = runner.invoke(check_command, ["non_existent_user"])
    assert result.exit_code == 0
    assert "User `non_existent_user` not found in the registry." in result.output


def test_list_command(runner, registry):
    result = runner.invoke(cli.list_command)
    assert result.exit_code == 0
    assert "extra_user" in result.output


def test_authenticate_command(runner, registry):
    result = runner.invoke(cli.authenticate_command, ["test_user_3"])
    assert result.exit_code == 0
    assert "Authenticated `test_user_3`" in result.output

    result = runner.invoke(cli.authenticate_command, ["default_user"], input="n\n")
    assert result.exit_code == 0
    assert "User `default_user` is already authenticated" in result.output
    assert "Cancelling" in result.output


def test_mark_default_user(runner, registry):
    """When listing users, make sure the default user is marked with *."""
    result = runner.invoke(cli.list_command)
    assert result.exit_code == 0
    assert "*" in result.output

    runner.invoke(cli.remove, ["default_user"])
    result = runner.invoke(cli.list_command)
    assert result.exit_code == 0
    assert "*" not in result.output
