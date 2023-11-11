import pytest
from click.testing import CliRunner

import eeauth.cli as cli


@pytest.fixture()
def runner():
    return CliRunner()


def test_activate_command_user_not_found(runner):
    result = runner.invoke(cli.activate, ["non_existent_user"])
    assert result.exit_code == 0
    assert "User `non_existent_user` not found in the registry." in result.output


def test_list_command(runner):
    result = runner.invoke(cli.list_command)
    assert result.exit_code == 0
    assert "Name" in result.output


def test_remove_command_user_not_found(runner):
    result = runner.invoke(cli.remove, ["non_existent_user"])
    assert result.exit_code == 0
    assert "User `non_existent_user` not found in the registry." in result.output
