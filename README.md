# mediajson

Type-aware json serialiser and deserialiser.

## Introduction

This library provides a custom JSON serialiser and deserialiser based on the ones in the standard python library but capable of
understanding a wider range of python types including the `mediatimestamps.timestamp` type and the `uuid.UUID` type, and
`fractions.Fraction` types.

## Installation

### Requirements

* A working Python 3.6+ installation
* The tool [tox](https://tox.readthedocs.io/en/latest/) is needed to run the unittests, but not required to use the library.

### Steps

```bash
# Install from pip
$ pip install mediatimestamp

# Install via apt-get
$ apt-get install python-mediatimestamp python3-mediatimestamp

# Install directly from source repo
$ git clone git@github.com:bbc/rd-apmm-python-lib-mediajson.git
$ cd rd-apmm-python-lib-mediajson
$ pip install -e .
```

## Usage

```python
import mediajson
import mediatimestamp

# Encode some json from a mediatimestamp.Timestamp object
print(mediajson.dumps(mediatimestamp.Timestamp.get_time()))
```

## Documentation

The API is well documented in the docstrings of the module mediajson, to view:

```bash
pydoc mediajson
```

## Development
### Testing

To run the unittests for this package in a virtual environment follow these steps:

```bash
$ git clone git@github.com:bbc/rd-apmm-python-lib-mediajson.git
$ cd rd-apmm-python-lib-mediajson
$ make test
```
### Packaging

Debian and RPM packages can be built using:

```bash
# Debian packaging
$ make deb

# RPM packageing
$ make rpm
```

### Continuous Integration

This repository includes a Jenkinsfile which makes use of custom steps defined in a BBC internal
library for use on our own Jenkins instances. As such it will not be immediately useable outside
of a BBC environment, but may still serve as inspiration and an example of how to implement CI
for this package.

## Versioning

We use [Semantic Versioning](https://semver.org/) for this repository

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

## Contributing

The code in this repository was previously released as part of the
nmos-common library (<https://github.com/bbc/nmos-common/>). For
contributing wok please see the file [CONTRIBUTING.md](./CONTRIBUTING.md) in this repository.

Please ensure you have run the test suite before submitting a Pull Request, and include a version bump in line with our [Versioning](#versioning) policy.

## Authors

* James Weaver (james.barrett@bbc.co.uk)
* Philip deNier (philip.denier@bbc.co.uk)
* Sam Nicholson (sam.nicholson@bbc.co.uk)

## License

See [LICENSE.md](LICENSE.md)
