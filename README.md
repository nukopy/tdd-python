# tdd-python

![pytest](https://github.com/nukopy/tdd-python/workflows/pytest/badge.svg?branch=master) [![codecov](https://codecov.io/gh/nukopy/tdd-python/branch/master/graph/badge.svg)](https://codecov.io/gh/nukopy/tdd-python)

## Requirements

- OS

```sh
$ sw_vers
ProductName:    Mac OS X
ProductVersion: 10.15.5
BuildVersion:   19F101
```

- Software Versions
  - Docker version 20.10.0, build 7287ab3
  - Docker Compose version 1.27.4, build 40524192

## Environment Setup

- git clone

```sh
git clone git@github.com:nukopy/tdd-python.git
```

- Build & Run Docker Container

```sh
cd tdd-python

# build Docker image
make dcb

# build & start container
make dcu
# Let's coding in VSCode extension "Remote - Containers"

# stop & remove container
make dcd
```

## Install `task_proj` locally

```sh
pip install ./lib/tasks_proj
```
