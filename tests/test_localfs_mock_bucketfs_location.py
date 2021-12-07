from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path

from exasol_bucketfs_utils_python.localfs_mock_bucketfs_location import LocalFSMockBucketFSLocation

def test_upload_download_string_from_different_instance():
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


def test_upload_download_obj_from_different_instance():
    with TemporaryDirectory() as path:
        bucketfs_location_upload = LocalFSMockBucketFSLocation(path)
        bucketfs_location_download = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_value = TestValue("test_string")
        bucketfs_location_upload.upload_object_to_bucketfs_via_joblib(test_value, bucket_file_path)
        result = bucketfs_location_download.download_object_from_bucketfs_via_joblib(bucket_file_path)
        assert result == test_value


def test_read_file_from_bucketfs_to_fileobj():
    with TemporaryDirectory() as path:
        bucketfs_location_read = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_byte_string = b"test_byte_string"
        with open(path + "/" + bucket_file_path, "wb") as file:
            file. write(test_byte_string)
            file.flush()
        with NamedTemporaryFile() as output_temp_file:
            bucketfs_location_read.read_file_from_bucketfs_to_fileobj(bucket_file_path,
                                                                output_temp_file)
            output_temp_file.flush()
            output_temp_file.seek(0)
            output_test_byte_string = output_temp_file.read()
            assert test_byte_string == output_test_byte_string


def test_read_file_from_bucketfs_to_file():
    with TemporaryDirectory() as path:
        bucketfs_location_read = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_byte_string = b"test_byte_string"
        with open(path + "/" + bucket_file_path, "wb") as file:
            file. write(test_byte_string)
            file.flush()
        with NamedTemporaryFile() as output_temp_file:
            bucketfs_location_read.read_file_from_bucketfs_to_file(bucket_file_path,
                                                                   Path(output_temp_file.name))
            output_test_byte_string = output_temp_file.read()
            assert test_byte_string == output_test_byte_string


def test_read_file_from_bucketfs_to_string():
    with TemporaryDirectory() as path:
        bucketfs_location_upload = LocalFSMockBucketFSLocation(path)
        bucketfs_location_read = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_string = "test_string"
        bucketfs_location_upload.upload_string_to_bucketfs(bucket_file_path, test_string)
        result = bucketfs_location_read.read_file_from_bucketfs_to_string(bucket_file_path)
        assert result == test_string


def test_read_file_from_bucketfs_via_joblib():
    with TemporaryDirectory() as path:
        bucketfs_location_upload = LocalFSMockBucketFSLocation(path)
        bucketfs_location_read = LocalFSMockBucketFSLocation(path)
        bucket_file_path = "test_file.txt"
        test_value = TestValue("test_string")
        bucketfs_location_upload.upload_object_to_bucketfs_via_joblib(test_value, bucket_file_path)
        result = bucketfs_location_read.read_file_from_bucketfs_via_joblib(bucket_file_path)
        assert result == test_value

