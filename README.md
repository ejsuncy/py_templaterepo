# py_templaterepo
![Current Version](https://img.shields.io/badge/Version-0.1.0a-brightgreen)

A python library for templaterepo.

## Installation

```bash
pip install py_templaterepo
```

## Usage
This library currently does not implement any rate limiting, so users of this library should implement their own 
rate limiting to avoid lockouts.

```python
import os
from py_templaterepo import Client

username = os.environ.get('ACCOUNT_USERNAME')
password = os.environ.get('ACCOUNT_PASSWORD')

client = Client(username, password)

# call the desired methods on the client; auth is handled automatically
```

## Contributing and Development

### Update git-submod-lib submodule for current Makefile Targets
```shell
git submodule update --init --remote
```

### Make Python venv and install requirements
```shell
make -f git-submod-lib/makefile/Makefile venv
```

Make and commit changes, and then build locally as follows.

### Build Locally
```shell
make -f git-submod-lib/makefile/Makefile build-python
```

### Make a pull request to `main` with your changes
```shell
make -f git-submod-lib/makefile/Makefile pull-request-main
```

## Releasing

### Minor releases
```shell
make -f git-submod-lib/makefile/Makefile promotion-alpha
```

Once the PR is approved and merged:
```shell
make -f git-submod-lib/makefile/Makefile github-release
```

Once the Release is published:
```shell
make -f git-submod-lib/makefile/Makefile twine-upload
```

Now cut a version release branch:
```shell
make -f git-submod-lib/makefile/Makefile github-branch
```

Now move `main` to the next `alpha` version to capture future development
```shell
make -f git-submod-lib/makefile/Makefile version-alpha
```

### Patch releases
Start with the version branch to be patched (ie `0.0.x`)
```shell
make -f git-submod-lib/makefile/Makefile promotion-patch
```

Once the PR is approved and merged:
```shell
make -f git-submod-lib/makefile/Makefile github-release-patch
```

Once the Patch Release is published:
```shell
make -f git-submod-lib/makefile/Makefile twine-upload
```
