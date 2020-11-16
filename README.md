# tdd-python

## Requirements

- OS

```sh
$ sw_vers
ProductName:    Mac OS X
ProductVersion: 10.15.5
BuildVersion:   19F101
```

- Software Versions
  - Python 3.9.0
  - Poetry 1.1.4

## Environment Setup

- git clone

```sh
git clone git@github.com:nukopy/tdd-python.git
```

- install Python packages with Poetry

```sh
cd tdd-python
python -m venv venv
source venv/bin/activate
pip install -U pip
poetry install
```

- execute tests

```sh
make test
```
