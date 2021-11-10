from pathlib import PurePosixPath

from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig

from exasol_bucketfs_utils_python.bucketfs_location import BucketFSLocation


def test_upload_download_string_with_different_instance():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6583, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig("bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    bucket_base_path = PurePosixPath("test")
    bucketfs_location_upload = BucketFSLocation(bucket_config, bucket_base_path)
    bucketfs_location_download = BucketFSLocation(bucket_config, bucket_base_path)
    bucket_file_path = "test_file.txt"
    test_string = "test_string"
    bucketfs_location_upload.upload_string_to_bucketfs(bucket_file_path, test_string)
    result = bucketfs_location_download.download_from_bucketfs_to_string(bucket_file_path)
    assert result == test_string


class TestValue():
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return self.value == self.value


def test_upload_download_obj_with_different_instance():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6583, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig("bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    bucket_base_path = PurePosixPath("test")
    bucketfs_location_upload = BucketFSLocation(bucket_config, bucket_base_path)
    bucketfs_location_download = BucketFSLocation(bucket_config, bucket_base_path)
    bucket_file_path = "test_file.txt"
    test_value = TestValue("test_string")
    bucketfs_location_upload.upload_object_to_bucketfs_via_joblib(test_value, bucket_file_path)
    result = bucketfs_location_download.download_object_from_bucketfs_via_joblib(bucket_file_path)
    assert result == test_value
