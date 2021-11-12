from tempfile import TemporaryDirectory

from exasol_bucketfs_utils_python.localfs_mock_bucketfs_location import LocalFSMockBucketFSLocation


def test_upload_download_string_with_different_instance():
    with TemporaryDirectory() as path:
        bucketfs_location_upload = LocalFSMockBucketFSLocation(path)
        bucketfs_location_download = LocalFSMockBucketFSLocation(path)
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
    with TemporaryDirectory() as path:
        bucketfs_location_upload = LocalFSMockBucketFSLocation(path)
        bucketfs_location_download = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_value = TestValue("test_string")
        bucketfs_location_upload.upload_object_to_bucketfs_via_joblib(test_value, bucket_file_path)
        result = bucketfs_location_download.download_object_from_bucketfs_via_joblib(bucket_file_path)
        assert result == test_value
