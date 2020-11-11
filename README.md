# BucketFS Utils Python

This project provides a python library for the Exasol BucketFS system.

Features:

* [Uploading a GitHub release to a bucket](#uploading-github-release-to-bucket)

## How to Use It

Install the package from Github via `pip`:
 
```
pip install -e git://github.com/exasol/bucketfs-utils-python.git@{ tag name }#egg=exasol-bucketfs-utils-python
```

## Uploading GitHub Release to Bucket

Example:

```python
from exasol_bucketfs_utils_python.github_release_file_bucketfs_uploader import GithubReleaseFileBucketFSUploader

release_uploader = \
    GithubReleaseFileBucketFSUploader(file_to_download_name="file",
                                        github_user="user",
                                        repository_name="repository",
                                        release_name="latest",
                                        path_inside_bucket="some/path/")
release_uploader.upload("http://<host>:<port>/<bucket>/", "user", "password")
```

### Run Time Dependencies

| Dependency                    | Purpose                          | License            |
|-------------------------------|----------------------------------|--------------------|
| [Python 3][python]            | Python version 3.6.1 and above   | PSF                |
| [Requests][requests]          | Allows to send HTTP/1.1 requests | Apache License 2.0 |


### Test Dependencies

| Dependency                    | Purpose                           | License           |
|-------------------------------|-----------------------------------|-------------------|
| [Pytest][pytest]              | Testing framework                 | MIT               |
| [Pytest Coverage][pytest-cov] | Tests coverage                    | MIT               |



[python]: https://docs.python.org
[requests]: https://pypi.org/project/requests/

[pytest]: https://docs.pytest.org/en/stable/
[pytest-cov]: https://pypi.org/project/pytest-cov/
