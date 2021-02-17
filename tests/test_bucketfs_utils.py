import pytest

from exasol_bucketfs_utils_python import bucketfs_utils
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSCredentials, BucketFsConfig


def test_get_bucketfs_udf_path_non_archive_file():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.get_bucketfs_udf_path(
        bucketfs_config=bucketfs_config,
        path_in_bucket="path/in/bucket/test_file.txt"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file.txt"

def test_get_bucketfs_udf_path_trailing_slash():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.get_bucketfs_udf_path(
        bucketfs_config=bucketfs_config,
        path_in_bucket="/path/in/bucket/test_file.txt"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file.txt"

@pytest.mark.parametrize("extension",["tar.gz","zip","tar.bz2","tar"])
def test_get_bucketfs_udf_path_archive_tar(extension):
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.get_bucketfs_udf_path(
        bucketfs_config=bucketfs_config,
        path_in_bucket=f"path/in/bucket/test_file.{extension}"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file/"

def test_generate_bucketfs_url_file():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.generate_bucketfs_url(
        bucketfs_config=bucketfs_config,
        path_in_bucket="path/in/bucket/test_file.txt"
    )
    assert udf_path == "http://localhost:6666/default/path/in/bucket/test_file.txt"

def test_generate_bucketfs_url_file_trailing_slash():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.generate_bucketfs_url(
        bucketfs_config=bucketfs_config,
        path_in_bucket="/path/in/bucket/test_file.txt"
    )
    assert udf_path == "http://localhost:6666/default/path/in/bucket/test_file.txt"

def test_generate_bucketfs_url_file_with_credentialsh():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    udf_path = bucketfs_utils.generate_bucketfs_url(
        bucketfs_config=bucketfs_config,
        path_in_bucket="path/in/bucket/test_file.txt",
        with_credentials=True
    )
    assert udf_path == "http://w:write@localhost:6666/default/path/in/bucket/test_file.txt"