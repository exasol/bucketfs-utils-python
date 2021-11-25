from pathlib import PurePosixPath

from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig

from exasol_bucketfs_utils_python.bucketfs_location import BucketFSLocation
import pytest
import textwrap
from tests.test_load_fs_file_from_udf import delete_testfile_from_BucketFS



def test_upload_download_string_with_different_instance():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
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


def test_upload_download_obj_with_different_instance(): #TODO better names?
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
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


    #TODO add new test for read functs
@pytest.mark.usefixtures("upload_language_container",
                             "pyexasol_connection",
                             "db_connection")
def test_read_files_to_str_from_bucketfs_inside_udf(upload_language_container, pyexasol_connection):
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
    bucketfs_config = BucketFSConfig("bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)
    bucket_base_path = PurePosixPath("test")
    bucketfs_location_upload = BucketFSLocation(bucket_config, bucket_base_path)
    bucket_file_path = "test_file.txt"
    test_string = "test_string"
    bucketfs_location_upload.upload_string_to_bucketfs(bucket_file_path, test_string)

    bucketfs_location_read = BucketFSLocation(bucket_config, bucket_base_path)

    try:

        # load file from udf
        target_schema = "TARGET_SCHEMA"
        pyexasol_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {target_schema};")  # mynotes dropfirst?
        pyexasol_connection.execute(f"OPEN SCHEMA {target_schema};")
        udf_sql = textwrap.dedent(f"""
            CREATE OR REPLACE PYTHON3_BFSUP SET SCRIPT {target_schema}."LoadFromLocalFS"(
                  "bucket_config" VARCHAR(2000000),
                  "path" VARCHAR(20000)
            )
            RETURNS VARCHAR(20000)
            AS 
            from exasol_bucketfs_utils_python.bucket_config import BucketConfig
            from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig
            from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
            from exasol_bucketfs_utils_python.bucketfs_location import BucketFSLocation
            from pathlib import PurePosixPath
            def get_bucket_config():
                bucket_name = "default"
                bucketfs_name = "bfsdefault"
                connection_config = BucketFSConnectionConfig(host="localhost",
                                                             port=6666,
                                                             user="r", pwd="read",
                                                             is_https=False)
                bucketfs_config = BucketFSConfig(bucketfs_name, connection_config=connection_config)
                return BucketConfig(bucket_name, bucketfs_config)

            def run(ctx):
                bucket_config = get_bucket_config()
                bucketfs_location_read = BucketFSLocation(bucket_config, PurePosixPath("test"))
                output_test_string = bucketfs_location_read.read_file_from_bucketfs_to_string(ctx.path)
                return output_test_string
            """)
        pyexasol_connection.execute(udf_sql)
        output_test_string = pyexasol_connection.execute(
            f"""select {target_schema}."LoadFromLocalFS"('{bucketfs_location_read.bucket_config}','{bucket_file_path}'
            )""").fetchall()
        assert output_test_string[0][0] == test_string
    finally:
        delete_testfile_from_BucketFS(file_path=bucket_file_path,
                                      bucket_config=bucketfs_location_read.bucket_config)
        pyexasol_connection.execute(f"DROP SCHEMA IF EXISTS {target_schema} CASCADE;")
