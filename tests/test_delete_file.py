from exasol_bucketfs_utils_python import upload, list_files, delete
from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig
from tests.test_load_fs_file_from_udf import delete_testfile_from_bucketfs


def test_delete_files():
    connection_config = BucketFSConnectionConfig(
        host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig(
        connection_config=connection_config, bucketfs_name="bfsdefault")
    bucket_config = BucketConfig(
        bucket_name="default", bucketfs_config=bucketfs_config)
    test_string = "test_string"

    path_list = ["path/in/bucket/file.txt", "path/file2.txt"]
    try:
        # upload files
        for path_in_bucket in path_list:
            upload.upload_string_to_bucketfs(
                bucket_config=bucket_config,
                bucket_file_path=path_in_bucket,
                string=test_string)

        bucket_file_path_map = {
            "path": ["in/bucket/file.txt", "file2.txt"],
            "path/in/bucket/": ["file.txt"]
        }

        # # check files exist
        for bucket_path, expected in bucket_file_path_map.items():
            listed_files = list_files.list_files_in_bucketfs(
                bucket_config, bucket_path)
            for listed_file in listed_files:
                assert listed_file in expected

        # delete files
        for path_in_bucket in path_list:
            delete.delete_file_in_bucketfs(
                bucket_config, path_in_bucket)

        # # check files not exist
        for bucket_path, expected in bucket_file_path_map.items():
            listed_files = list_files.list_files_in_bucketfs(
                bucket_config, bucket_path)
            print(listed_files)
            for listed_file in listed_files:
                assert listed_file not in expected
                print(listed_file)
    finally:
        for path_in_bucket in path_list:
            delete_testfile_from_bucketfs(
                file_path=path_in_bucket,
                bucket_config=bucket_config)
