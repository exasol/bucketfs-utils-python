import pytest
from pathlib import PurePosixPath
from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import \
    BucketFSConnectionConfig
from exasol_bucketfs_utils_python.bucketfs_location import BucketFSLocation
from tests.integration_tests.with_db.test_load_fs_file_from_udf import \
    delete_testfile_from_bucketfs


# TODO replace upload_testfile_to_BucketFS once missing funcs in BucketFSLocation are implemented


@pytest.mark.parametrize("path_in_bucket, expected_path_in_bucket", [
    ("/path/in/bucket/file.txt", "path/in/bucket/file.txt"),
    ("path/in/bucket/file.txt", "path/in/bucket/file.txt"),
    ("", ""),
    (None, "")])
def test_get_complete_file_path_in_bucket_with_base_path(
        path_in_bucket, expected_path_in_bucket):

    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)

    base_path = "base_path"
    bucketfs_location = BucketFSLocation(
        bucket_config=bucket_config, base_path=PurePosixPath(base_path))

    complete_file_path_in_bucket = bucketfs_location\
        .get_complete_file_path_in_bucket(path_in_bucket)
    assert complete_file_path_in_bucket == \
           str(PurePosixPath(base_path, expected_path_in_bucket))


@pytest.mark.parametrize("path_in_bucket, expected_path_in_bucket", [
    ("/path/in/bucket/file.txt", "path/in/bucket/file.txt"),
    ("path/in/bucket/file.txt", "path/in/bucket/file.txt"),
    ("", ""),
    (None, "")])
def test_get_complete_file_path_in_bucket_without_base_path(
        path_in_bucket, expected_path_in_bucket):

    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)

    bucketfs_location = BucketFSLocation(
        bucket_config=bucket_config, base_path=None)

    complete_file_path_in_bucket = bucketfs_location\
        .get_complete_file_path_in_bucket(path_in_bucket)
    assert complete_file_path_in_bucket == \
           str(PurePosixPath(expected_path_in_bucket))


@pytest.mark.parametrize("path_in_bucket", [
    "/path/in/bucket/file.txt",
    "path/in/bucket/file.txt",
    "path/in/bucket/file.txt.tar.gz",
    "path/in/bucket/file.txt.zip",
    "path/in/bucket/file.txt.tgz",
    "path/in/bucket/file.txt.tar"])
def test_generate_bucket_udf_path_with_base_path(path_in_bucket):
    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)

    base_path = "base_path"
    bucketfs_location = BucketFSLocation(
        bucket_config=bucket_config, base_path=PurePosixPath(base_path))
    udf_path = bucketfs_location.generate_bucket_udf_path(
        path_in_bucket=path_in_bucket)

    assert str(udf_path) == \
           f"/buckets/bfsdefault/default/{base_path}/path/in/bucket/file.txt"


@pytest.mark.parametrize("path_in_bucket", [
    "/path/in/bucket/file.txt",
    "path/in/bucket/file.txt",
    "path/in/bucket/file.txt.tar.gz",
    "path/in/bucket/file.txt.zip",
    "path/in/bucket/file.txt.tgz",
    "path/in/bucket/file.txt.tar"])
def test_generate_bucket_udf_path_without_base_path(path_in_bucket):
    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)

    bucketfs_location = BucketFSLocation(
        bucket_config=bucket_config, base_path=None)
    udf_path = bucketfs_location.generate_bucket_udf_path(
        path_in_bucket=path_in_bucket)

    assert str(udf_path) == \
           "/buckets/bfsdefault/default/path/in/bucket/file.txt"


def test_upload_download_string_from_different_instance():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig("bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    bucket_base_path = PurePosixPath("test_up_down_str")
    bucketfs_location_upload = BucketFSLocation(bucket_config, bucket_base_path)
    bucketfs_location_download = BucketFSLocation(bucket_config, bucket_base_path)
    bucket_file_path = "test_file.txt"
    test_string = "test_string"
    bucketfs_location_upload.upload_string_to_bucketfs(bucket_file_path, test_string)
    result = bucketfs_location_download.download_from_bucketfs_to_string(bucket_file_path)
    assert result == test_string
    delete_testfile_from_bucketfs(file_path=str(bucket_base_path) + "/" + bucket_file_path,
                                  bucket_config=bucketfs_location_upload.bucket_config)


class TestValue:
    __test__ = False

    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return self.value == self.value


def test_upload_download_obj_from_different_instance():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig("bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    bucket_base_path = PurePosixPath("test_up_down_obj")
    bucketfs_location_upload = BucketFSLocation(bucket_config, bucket_base_path)
    bucketfs_location_download = BucketFSLocation(bucket_config, bucket_base_path)
    bucket_file_path = "test_file.txt"
    test_value = TestValue("test_string")
    bucketfs_location_upload.upload_object_to_bucketfs_via_joblib(test_value, bucket_file_path)
    result = bucketfs_location_download.download_object_from_bucketfs_via_joblib(bucket_file_path)
    assert result == test_value
    delete_testfile_from_bucketfs(file_path=str(bucket_base_path) + "/" + bucket_file_path,
                                  bucket_config=bucketfs_location_upload.bucket_config)
