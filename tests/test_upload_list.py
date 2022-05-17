from exasol_bucketfs_utils_python import upload, list_files
from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig
from tests.test_load_fs_file_from_udf import delete_testfile_from_bucketfs


def test_list_files():
    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)
    test_string = "test_string"

    path_list = ["path/in/bucket/file.txt", "path/file2.txt"]
    try:
        for path_in_bucket in path_list:
            upload.upload_string_to_bucketfs(
                bucket_config=bucket_config,
                bucket_file_path=path_in_bucket,
                string=test_string)

        bucket_file_path_map = {
            "path": ["in/bucket/file.txt", "file2.txt"],
            "path/": ["in/bucket/file.txt", "file2.txt"],
            "path/in": ["bucket/file.txt"],
            "path/in/": ["bucket/file.txt"],
            "path/in/bucket": ["file.txt"],
            "path/in/bucket/": ["file.txt"],
            "path/in/bucket/file.txt": [],
            ".": ["path/in/bucket/file.txt", "path/file2.txt"]
        }
        for bucket_path, expected in bucket_file_path_map.items():
            assert set(expected) == set(list_files.list_files_in_bucketfs(
                bucket_config, bucket_path))
    finally:
        for path_in_bucket in path_list:
            delete_testfile_from_bucketfs(
                file_path=path_in_bucket,
                bucket_config=bucket_config)
