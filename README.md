# eeauth

[![Earth Engine Python](https://img.shields.io/badge/Earth%20Engine%20API-Python-green)](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)
[![PyPI version](https://badge.fury.io/py/eeauth.svg)](https://badge.fury.io/py/eeauth)
[![Build status](https://github.com/aazuspan/eeauth/actions/workflows/ci.yaml/badge.svg)](https://github.com/aazuspan/eeauth/actions/workflows/ci.yaml)


An account manager for the Earth Engine Python API that lets you easily authenticate and switch between multiple Google accounts.

## Installation

### From PyPI

```bash
pip install eeauth
```

### From conda-forge

*Coming soon!*

## Usage

### Authenticate

Import `eeauth`, then authenticate a user by running `ee.Authenticate.as_user("username")` and following the usual authentication instructions, being sure to select the correct Google account[^username]. The credentials for each authenticated user are stored by `eeauth` for later use.

```python
import ee
import eeauth

# Authenticate and register credentials for multiple accounts
ee.Authenticate.as_user("personal")
ee.Authenticate.as_user("work")
```

### Initialize

With two users authenticated, you can now initialize Earth Engine with a specific user and switch between them at will.

```python
# Get tasks from your "personal" account
ee.Initialize.as_user("personal")
ee.data.getTaskList()

# And from your "work" account
ee.Initialize.as_user("work")
ee.data.getTaskList()
```

### CLI

The `eeauth` command line interface lets you manage your authenticated users from the terminal.

```bash
Usage: eeauth [OPTIONS] COMMAND [ARGS]...

  Manage Earth Engine authentication.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  activate      Set USER as the default Earth Engine user.
  authenticate  Authenticate USER and store their credentials.
  list          List all authenticated users.
  remove        Remove USER from the registry.
```


## FAQ

### How does it work?

When you run `ee.Authenticate()`, Earth Engine stores a single credential file on your local machine. To initialize with a different account, you typically need to repeat the authentication process, replacing your old credentials with new credentials. `eeauth` allows you to store multiple credentials tied to unique usernames, so that you can quickly switch between authenticated users without the hassle of re-authenticating every time.

### Can I still use `ee.Initialize()`?

Earth Engine will continue to store the most recently authenticated credentials, so `ee.Initialize()` will work like it always has. You can also run `eeauth activate [USER]` in a terminal to change which user gets initialized by default.

### Is it safe?

Like Earth Engine, `eeauth` stores your credentials in an unencrypted local file[^registry]. As long as you don't share that file, you should be good to go.

### Why do I have to run `import eeauth`?

Importing the package adds the `as_user` functions to `ee.Authenticate` and `ee.Initialize`. 

[^registry]: Credentials are stored in `~/.config/eeauth/registry.json`.
[^username]: Usernames do not need to match the name of your Google account.
