# mediajson

Type-aware json serialiser and deserialiser.

## Introduction

This library provides a custom JSON serialiser and deserialiser based on the ones in the standard python library but capable of
understanding a wider range of python types including the `mediatimestamps.timestamp` type and the `uuid.UUID` type, and
`fractions.Fraction` types.

## Installation

### Requirements

* A working Python 3.10+ installation
* The tool [Docker](https://docs.docker.com/engine/install/) is needed to run the tests, but not required to use the library.

### Steps

```bash
# Install from pip
$ pip install mediatimestamp

# Install directly from source repo
$ git clone git@github.com:bbc/rd-apmm-python-lib-mediajson.git
$ cd rd-apmm-python-lib-mediajson
$ make install
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
make docs
```
This command will render documentation as HTML in the `/docs` directory.

## Development
### Commontooling

This repository uses a library of makefiles, templates, and other tools for development tooling and CI workflows. To discover operations that may be run against this repo, run the following in the top level of the repo:

```bash
$ make
```

### Testing

To run the unittests for this package in a docker container follow these steps:

```bash
$ git clone git@github.com:bbc/rd-apmm-python-lib-mediajson.git
$ cd rd-apmm-python-lib-mediajson
$ make test
```

### Continuous Integration

This repository includes a Jenkinsfile which makes use of custom steps defined in a BBC internal
library for use on our own Jenkins instances. As such it will not be immediately useable outside
of a BBC environment, but may still serve as inspiration and an example of how to implement CI
for this package.

## Versioning

We use [Semantic Versioning](https://semver.org/) for this repository

## Contributing

The code in this repository was previously released as part of the
nmos-common library (<https://github.com/bbc/nmos-common/>). For
contributing work please see the file [CONTRIBUTING.md](./CONTRIBUTING.md) in this repository.

Please ensure you have run the test suite before submitting a Pull Request, and include a version bump in line with our [Versioning](#versioning) policy.

## Authors

* James Weaver
* Philip deNier
* Sam Mesterton-Gibbons
* James Sandford

For further information, contact <cloudfit-opensource@rd.bbc.co.uk>

## License

See [LICENSE.md](LICENSE.md)
