# eeauth

An account manager for the Earth Engine Python API that lets you easily authenticate and switch between multiple Google accounts.

## Installation

*PyPI and conda-forge coming soon!*

### From Source

```bash
pip install git+https://github.com/aazuspan/eeauth.git
```

## Usage

### Authenticate

First, import `eeauth` to attach new functions to `ee.Authenticate` and `ee.Initialize`. Next, authenticate a user by running `ee.Authenticate.as_user("username")` and following the usual authentication instructions, being sure to select the correct Google account[^username]. You can authenticate as many different users as needed, and `eeauth` will store their credentials so that they can be retrieved when needed.

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

### Helpers

`eeauth` contains some other helpful functions for managing Earth Engine authentication.

```python
>>> # Get the name of the initialized user
>>> eeauth.get_initialized_user()
"work"

>>> # List the currently registered users
>>> eeauth.list_users()
["personal", "work"]

>>> # Set the default user for `ee.Initialize()`
>>> eeauth.activate_user("personal")

>>> # Delete a set of credentials
>>> eeauth.remove_user("work")
>>> eeauth.list_users()
["personal"]

>>> # Delete all stored credentials
>>> eeauth.reset()
>>> eeauth.list_users()
[]
```


## FAQ[^faq]

### How does it work?

Typically when you use `ee.Authenticate()` and `ee.Initialize()`, Earth Engine stores a single credential file on your local machine. To switch accounts, you need to repeat the authentication process, replacing your old credentials with new credentials. `eeauth` allows you to store multiple credentials tied to unique usernames, so that you can quickly switch between authenticated users without the hassle of re-authenticating every time.

### Can I still use `ee.Initialize()`?

Sure! Earth Engine will continue to store the most recently authenticated credentials, so `ee.Initialize()` will work like it always has. You can also use `eeauth.activate_user` to change which user gets initialized by default.

### Is it safe?

Like Earth Engine, `eeauth` stores your credentials in an unencrypted local file (`~/.config/eeauth/registry.json`). As long as you don't share that file, you should be good to go.

### Why do I have to run `import eeauth`?

Importing the package adds the `as_user` functions to `ee.Authenticate` and `ee.Initialize`. 

[^username]: Usernames do not need to match the name of your Google account.
[^faq]: Nobody actually asked me these, I just figured they might. That's how FAQ's always work, right?