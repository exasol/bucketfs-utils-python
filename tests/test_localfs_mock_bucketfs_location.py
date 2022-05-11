from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path, PurePosixPath

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


class TestValue:
    __test__ = False

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


def test_upload_read_fileobject ():
    tmp_file_fname = "tmp_file_path.txt"
    input_test_byte_string = b"test_byte_string"

    with TemporaryDirectory() as path:
        bucketfs_location = LocalFSMockBucketFSLocation(path)

        with NamedTemporaryFile() as input_tmp_file:
            input_tmp_file.write(input_test_byte_string)
            input_tmp_file.flush()
            input_tmp_file.seek(0)
            bucketfs_location.upload_fileobj_to_bucketfs(
                input_tmp_file, str(PurePosixPath(path, tmp_file_fname)))

        with NamedTemporaryFile() as output_tmp_file:
            bucketfs_location.read_file_from_bucketfs_to_fileobj(
                str(PurePosixPath(path, tmp_file_fname)), output_tmp_file)
            output_tmp_file.flush()
            output_tmp_file.seek(0)
            output_test_byte_string = output_tmp_file.read()

    assert input_test_byte_string == output_test_byte_string
