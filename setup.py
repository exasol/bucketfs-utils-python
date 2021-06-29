# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol_bucketfs_utils_python']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.1,<2.0.0', 'requests>=2.24.0,<3.0.0', 'typeguard>=2.11.1,<3.0.0']

setup_kwargs = {
    'name': 'exasol-bucketfs-utils-python',
    'version': '0.1.0',
    'description': 'BucketFS utilities for the Python programming language',
    'long_description': '#####################\nBucketFS Utils Python\n#####################\n\n********\nOverview\n********\n\nThis project provides a python library for accessing the Exasol BucketFS system.\nIt provides functions to upload and download files to and from the BucketFS.\n\nIn a Nutshell\n=============\n\nPrerequisites\n-------------\n\n- Python 3.6+\n\nInstallation\n-------------\n\nInstall the package from Github via `pip`::\n\n    pip install -e git://github.com/exasol/bucketfs-utils-python.git@{tag name}#egg=exasol-bucketfs-utils-python\n\nDocumentation\n-------------\n\n`Documentation for the latest release text <https://exasol.github.io/bucketfs-utils-python/main>`_ is hosted on the Github Pages of this project.\n\nFeatures\n========\n\n* Download or upload files from/to the Exasol BucketFS\n* Supported sources and targets for the uploads and downloads:\n\n  * Files on the local Filesystem\n  * Python file objects\n  * Python Strings\n  * Python objects ((De-)Serialization with [Joblib](https://joblib.readthedocs.io/en/latest/persistence.html))\n\n* Loading an artefact from a public Github Release into the BucketFS\n',
    'author': 'Torsten Kilias',
    'author_email': 'torsten.kilias@exasol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exasol/bucketfs-utils-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
