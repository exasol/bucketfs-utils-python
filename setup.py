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
    'long_description': '#####################\nBucketFS Utils Python\n#####################\n\n.. include:: doc/overview.rst\n\n*****************\nTable of Contents\n*****************\n.. include::doc/overview.rst\n\nInformation for Users\n=====================\n\n* [User Guide](doc/user_guide/user_guide.md)\n* [Changelog](doc/changes/changelog.md)\n\nInformation for Developers\n==========================\n\n* [Developer Guide](doc/developer_guide/developer_guide.md)\n* [Dependencies](doc/dependencies.md)\n\n',
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
