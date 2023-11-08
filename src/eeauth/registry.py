import json
from collections import UserDict
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

from .errors import UserNotFoundError

REGISTRY_PATH = Path("~/.config/eeauth/registry.json").expanduser()


class _FileDict(UserDict):
    """
    A dict-like context manager that reads and writes to a linked JSON file.
    """

    def __init__(self, path):
        self.path = Path(path)
        super().__init__()

    def __enter__(self):
        """On enter, create the JSON file and read the current data."""
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._write_json()

        self.data = self._read_json()
        self._init_data = deepcopy(self.data)

        return self

    def __exit__(self, *_):
        """On exit, write out any updated data to the JSON file."""
        if self.data != self._init_data:
            self._write_json()

    def _read_json(self):
        """Read from JSON."""
        with open(self.path) as f:
            return json.load(f)

    def _write_json(self):
        """Write to JSON."""
        with open(self.path, "w") as f:
            json.dump(self.data, f)


class _ReadOnlyFileDict(_FileDict):
    """
    An immutable dict-like context manager that reads from a linked JSON file.

    Notes
    -----
    Changes can be made to the underlying `data` attribute, but they will not be
    persisted to the file.
    """

    def __exit__(self, *_):
        """Exit without writing."""
        return

    def __setitem__(self, *_) -> None:
        """Prevent setting."""
        raise TypeError("Cannot set items from read-only file dict.")

    def __delitem__(self, *_) -> None:
        """Prevent deleting."""
        raise TypeError("Cannot delete items from read-only file dict.")


class _UserRegistry(_FileDict):
    """
    A _FileDict of user credentials.
    """

    def __delitem__(self, key):
        try:
            super().__delitem__(key)
        except KeyError:
            raise UserNotFoundError(key) from None

    def __missing__(self, key):
        raise UserNotFoundError(key)


class _ReadOnlyUserRegistry(_ReadOnlyFileDict, _UserRegistry):
    """
    A _ReadOnlyFileDict of user credentials.
    """

    pass


@contextmanager
def open_user_registry(path=None, read_only=True):
    """
    Open the JSON user registry as a dict-like context manager.

    Parameters
    ----------
    path : str
        Path to the JSON file.
    read_only : bool, optional
        If True, changes cannot be made to the underlying data.

    Examples
    --------
    >>> with open_user_registry("path/to/file.json") as fd:
    ...     fd["key"] = "value"
    """
    path = path or REGISTRY_PATH
    manager = _ReadOnlyUserRegistry if read_only else _UserRegistry

    with manager(path) as fd:
        yield fd
