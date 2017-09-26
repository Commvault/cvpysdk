#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Setup file for the CVPySDK Python package."""

import os
import re
import ssl

from setuptools import setup, find_packages


ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.dirname(__file__)
VERSION = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    """Gets the version of the CVPySDK python package from __init__.py file."""
    init = open(os.path.join(ROOT, 'cvpysdk', '__init__.py')).read()
    return VERSION.search(init).group(1)


def readme():
    """Reads the README.rst file and returns its contents."""
    read_me_file = os.path.join(ROOT, 'README.rst')
    with open(read_me_file) as file_object:
        return file_object.read()


def get_license():
    """Reads the LICENSE.txt file and returns its contents."""
    license_file = os.path.join(ROOT, 'LICENSE.txt')
    with open(license_file) as file_object:
        return file_object.read()

setup(
    name='cvpysdk',
    version=get_version(),
    author='Commvault Systems Inc.',
    author_email='Dev-PythonSDK@commvault.com',
    description='Commvault SDK for Python',
    license=get_license(),
    long_description=readme(),
    url='https://github.com/CommvaultEngg/cvpysdk',
    scripts=[],
    packages=find_packages(),
    keywords='commvault, python, sdk, cv, simpana, commcell, cvlt, webconsole',
    include_package_data=True,
    install_requires=['requests', 'future', 'xmltodict'],
    zip_safe=False
)
