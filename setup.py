#!/usr/bin/env python3
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

from setuptools import setup

# Basic metadata
name = 'mediajson'
description = 'A JSON serialiser and parser for python that supports extensions convenient for our media grain formats'
url = 'https://github.com/bbc/rd-apmm-python-lib-mediajson'
author = u'BBC R&D'
author_email = u'cloudfit-opensource@rd.bbc.co.uk'
license = 'Apache 2'
long_description = description


# Execute version file to set version variable
try:
    with open(("{}/_version.py".format(name)), "r") as fp:
        exec(fp.read())
except IOError:
    # Version file doesn't exist, fake it for now
    __version__ = "0.0.0"

package_names = [
    'mediajson'
]
packages = {
    pkg: pkg.replace('.', '/') for pkg in package_names
}

# This is where you list packages which are required
packages_required = [
    "mediatimestamp >= 4.0.0",
    "typing_extensions"
]

setup(name=name,
      python_requires='>=3.10.0',
      version=__version__,
      description=description,
      url=url,
      author=author,
      author_email=author_email,
      license=license,
      packages=package_names,
      package_dir=packages,
      package_data={package_name: ['py.typed'] for package_name in package_names},
      install_requires=packages_required,
      scripts=[],
      data_files=[],
      long_description=long_description)
