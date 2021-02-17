from pathlib import Path
from tempfile import NamedTemporaryFile

from exasol_bucketfs_utils_python import upload, download
from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig, BucketFSCredentials


def test_file_upload_download():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    with NamedTemporaryFile() as input_temp_file:
        test_byte_string = b"test_byte_string"
        input_temp_file.write(test_byte_string)
        input_temp_file.flush()

        path_in_bucket = "path/in/bucket/file.txt"
        upload.upload_file_to_bucketfs(
            bucketfs_config=bucketfs_config,
            bucket_file_path=path_in_bucket,
            local_file_path=Path(input_temp_file.name))

        with NamedTemporaryFile() as output_temp_file:
            download.download_from_bucketfs_to_file(
                bucketfs_config=bucketfs_config,
                bucket_file_path=path_in_bucket,
                local_file_path=Path(output_temp_file.name))
            output_test_byte_string = output_temp_file.read()
            assert test_byte_string == output_test_byte_string


def test_fileobj_upload_download():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    with NamedTemporaryFile() as input_temp_file:
        test_byte_string = b"test_byte_string"
        input_temp_file.write(test_byte_string)
        input_temp_file.flush()
        input_temp_file.seek(0)
        path_in_bucket = "path/in/bucket/file.txt"
        upload.upload_fileobj_to_bucketfs(
            bucketfs_config=bucketfs_config,
            bucket_file_path=path_in_bucket,
            fileobj=input_temp_file)

        with NamedTemporaryFile() as output_temp_file:
            download.download_from_bucketfs_to_fileobj(
                bucketfs_config=bucketfs_config,
                bucket_file_path=path_in_bucket,
                fileobj=output_temp_file)
            output_temp_file.flush()
            output_temp_file.seek(0)
            output_test_byte_string = output_temp_file.read()
            assert test_byte_string == output_test_byte_string


def test_string_upload_download():
    bucketfs_credentials = BucketFSCredentials(host="localhost", port="6666", user="w", pwd="write")
    bucketfs_config = BucketFsConfig(credentials=bucketfs_credentials,
                                     bucket="default",
                                     bucketfs_name="bfsdefault",
                                     is_https=False)
    test_string = "test_string"
    path_in_bucket = "path/in/bucket/file.txt"
    upload.upload_string_to_bucketfs(
        bucketfs_config=bucketfs_config,
        bucket_file_path=path_in_bucket,
        string=test_string)

    output_test_string = \
        download.download_from_bucketfs_to_string(
            bucketfs_config=bucketfs_config,
            bucket_file_path=path_in_bucket)

    assert test_string == output_test_string