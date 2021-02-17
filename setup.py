# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol_bucketfs_utils_python']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'exasol-bucketfs-utils-python',
    'version': '0.1.0',
    'description': 'BucketFS utilities for the Python programming language',
    'long_description': '# BucketFS Utils Python\n\nThis project provides a python library for the Exasol BucketFS system.\n\nFeatures:\n\n* [Uploading a GitHub release to a bucket](#uploading-github-release-to-bucket)\n\n## How to Use It\n\nInstall the package from Github via `pip`:\n \n```\npip install -e git://github.com/exasol/bucketfs-utils-python.git@{ tag name }#egg=exasol-bucketfs-utils-python\n```\n\n## Uploading GitHub Release to Bucket\n\nExample:\n\n```python\nfrom exasol_bucketfs_utils_python.github_release_file_bucketfs_uploader import GithubReleaseFileBucketFSUploader\n\nrelease_uploader = \\\n    GithubReleaseFileBucketFSUploader(file_to_download_name="file",\n                                        github_user="user",\n                                        repository_name="repository",\n                                        release_name="latest",\n                                        path_inside_bucket="some/path/")\nrelease_uploader.upload("http://<host>:<port>/<bucket>/", "user", "password")\n```\n\n### Run Time Dependencies\n\n| Dependency                    | Purpose                          | License            |\n|-------------------------------|----------------------------------|--------------------|\n| [Python 3][python]            | Python version 3.6.1 and above   | PSF                |\n| [Requests][requests]          | Allows to send HTTP/1.1 requests | Apache License 2.0 |\n\n\n### Test Dependencies\n\n| Dependency                    | Purpose                           | License           |\n|-------------------------------|-----------------------------------|-------------------|\n| [Pytest][pytest]              | Testing framework                 | MIT               |\n| [Pytest Coverage][pytest-cov] | Tests coverage                    | MIT               |\n\n\n\n[python]: https://docs.python.org\n[requests]: https://pypi.org/project/requests/\n\n[pytest]: https://docs.pytest.org/en/stable/\n[pytest-cov]: https://pypi.org/project/pytest-cov/\n',
    'author': 'Torsten Kilias',
    'author_email': 'torsten.kilias@exasol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exasol/bucketfs-utils-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
