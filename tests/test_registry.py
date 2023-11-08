import json
import os

import pytest

from eeauth.registry import open_user_registry


@pytest.fixture()
def file_path(tmpdir):
    file_path = os.path.join(tmpdir, "test.json")
    with open(file_path, "w") as f:
        json.dump({"key": "value"}, f)
    return file_path


def test_open_user_registry_creates_missing_file(tmpdir):
    file_path = os.path.join(tmpdir, "nonexistent.json")
    assert not os.path.exists(file_path)
    with open_user_registry(file_path, read_only=False) as fd:
        fd["key"] = "value"

    assert os.path.exists(file_path)


def test_open_user_registry_is_read_only(file_path):
    with open_user_registry(file_path) as fd:
        assert fd["key"] == "value"
        with pytest.raises(TypeError):
            fd["key"] = "new_value"
        with pytest.raises(TypeError):
            del fd["key"]


def test_open_user_registry_is_writable(file_path):
    with open_user_registry(file_path, read_only=False) as fd:
        assert fd["key"] == "value"
        fd["key"] = "new_value"

    with open(file_path) as f:
        data = json.load(f)
        assert data["key"] == "new_value"
