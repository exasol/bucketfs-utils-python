import pytest

from exasol_bucketfs_utils_python import bucketfs_utils
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConnectionConfig, BucketFsConfig, BucketConfig


def test_get_bucket_udf_path_non_archive_file():
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.get_bucket_udf_path(
        bucket_config=bucket_config,
        path_in_bucket="path/in/bucket/test_file.txt"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file.txt"


def test_get_bucket_udf_path_trailing_slash():
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.get_bucket_udf_path(
        bucket_config=bucket_config,
        path_in_bucket="/path/in/bucket/test_file.txt"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file.txt"


@pytest.mark.parametrize("extension", ["tar.gz", "zip", "tar.bz2", "tar"])
def test_get_bucket_udf_path_archive_tar(extension):
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.get_bucket_udf_path(
        bucket_config=bucket_config,
        path_in_bucket=f"path/in/bucket/test_file.{extension}"
    )
    assert udf_path == "/buckets/bfsdefault/default/path/in/bucket/test_file"


def test_generate_bucket_url_file():
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.generate_bucket_url(
        bucket_config=bucket_config,
        path_in_bucket="path/in/bucket/test_file.txt"
    )
    assert udf_path == "http://localhost:6666/default/path/in/bucket/test_file.txt"


def test_generate_bucket_url_file_trailing_slash():
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.generate_bucket_url(
        bucket_config=bucket_config,
        path_in_bucket="/path/in/bucket/test_file.txt"
    )
    assert udf_path == "http://localhost:6666/default/path/in/bucket/test_file.txt"


def test_generate_bucket_url_file_with_credentialsh():
    connection_config = BucketFSConnectionConfig(host="localhost", port="6666", user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFsConfig(connection_config=connection_config,
                                     bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    udf_path = bucketfs_utils.generate_bucket_url(
        bucket_config=bucket_config,
        path_in_bucket="path/in/bucket/test_file.txt",
        with_credentials=True
    )
    assert udf_path == "http://w:write@localhost:6666/default/path/in/bucket/test_file.txt"
