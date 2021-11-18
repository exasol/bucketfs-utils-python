import textwrap
from pathlib import Path

import pyexasol
import pytest
from tempfile import NamedTemporaryFile

from exasol_udf_mock_python.connection import Connection
                                                            #TODO something is strange with poetry install of
                                                            # exasol_udf_mock_python and dill

from exasol_bucketfs_utils_python.bucketfs_factory import BucketFSFactory
from exasol_bucketfs_utils_python import upload


@pytest.fixture(scope="session")
def db_connection():
    db_connection = Connection(address=f"localhost:8888", user="sys", password="exasol")
    return db_connection


@pytest.fixture(scope="session")
def pyexasol_connection(db_connection):
    conn = pyexasol.connect(dsn=db_connection.address, user=db_connection.user, password=db_connection.password)
    return conn

#mynote : this is needed to use language container
@pytest.fixture(scope="session")
def upload_language_container(pyexasol_connection, language_container):
    container_connection = Connection(address=f"http://localhost:6666/default/container;bfsdefault",
                                      user="w", password="write")
    bucket_fs_factory = BucketFSFactory()
    container_bucketfs_location = \
        bucket_fs_factory.create_bucketfs_location(
            url=container_connection.address,
            user=container_connection.user,
            pwd=container_connection.password,
            base_path=None)
    container_path = Path(language_container["container_path"])
    alter_session = Path(language_container["alter_session"])
    pyexasol_connection.execute(f"ALTER SYSTEM SET SCRIPT_LANGUAGES='{alter_session}'")
    pyexasol_connection.execute(f"ALTER SESSION SET SCRIPT_LANGUAGES='{alter_session}'")
    with open(container_path, "rb") as container_file:
        container_bucketfs_location.upload_fileobj_to_bucketfs(container_file, "ml.tar")


@pytest.fixture(scope="session")
def bucketfs_location():
    container_connection = Connection(address=f"http://localhost:6666/default/container;bfsdefault",
                                      user="w", password="write")
    bucket_fs_factory = BucketFSFactory()
    container_bucketfs_location = \
        bucket_fs_factory.create_bucketfs_location(
            url=container_connection.address,
            user=container_connection.user,
            pwd=container_connection.password,
            base_path=None)
    return container_bucketfs_location


#@pytest.fixture(scope="session")
#def bucket_config():
#    bucket_name = "default"
#    bucketfs_name = "bfsdefault"
#    connection_config = BucketFSConnectionConfig(host="localhost",
#                                                 port=6666,
#                                                 user="r", pwd="read",
#                                                 is_https=False)
#    bucketfs_config = BucketFSConfig(bucketfs_name, connection_config=connection_config)
#    bucket_config = BucketConfig(bucket_name, bucketfs_config)


# TODO write  actual tests
# TODO test for missing file? test for wrong file format, invalid bucket obj, error while writing?


def test_load_file_to_string(upload_language_container, pyexasol_connection, bucketfs_location, bucket_config):
    test_input_string = "test_byte_string"
    # upload file
    with NamedTemporaryFile() as input_temp_file:
        input_temp_file.write(test_input_string.encode('utf-8'))
        input_temp_file.flush()

        path_in_bucket = "path/in/bucket/file.txt"
        upload.upload_file_to_bucketfs(
            bucket_config=bucketfs_location.bucket_config,
            bucket_file_path=path_in_bucket,
            local_file_path=Path(input_temp_file.name))
        try:

            # load file from udf
            target_schema = "TARGET_SCHEMA"
            pyexasol_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {target_schema};") #mynotes dropfirst?
            pyexasol_connection.execute(f"OPEN SCHEMA {target_schema};")
            udf_sql = textwrap.dedent(f"""
                CREATE OR REPLACE PYTHON3_BFSUP SET SCRIPT {target_schema}."LoadFsFileFrom_UDF"(
                      "bucket_config" VARCHAR(2000000),
                      "path" VARCHAR(20000)
                )
                RETURNS VARCHAR(20000)
                AS 
                from exasol_bucketfs_utils_python.bucket_config import BucketConfig
                from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig
                from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
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
                    from exasol_bucketfs_utils_python.load_fs_file_from_udf import LoadFsFileFromUDF
                    udf = LoadFsFileFromUDF()
                    x = udf.run(ctx, exa, bucket_config)
                    return x
                """)
            pyexasol_connection.execute(udf_sql)
            #TODO how get bucket config in there? or is this ok?
            output_test_string = pyexasol_connection.execute(
                f"""select {target_schema}."LoadFsFileFrom_UDF"('{bucketfs_location.bucket_config}','{path_in_bucket}'
                )""").fetchall()
            assert output_test_string == test_input_string
    #TODO delete file?
        finally:
            pyexasol_connection.execute(f"DROP SCHEMA IF EXISTS {target_schema} CASCADE;")


def test_load_file_to_fileObj(pyexasol_connection):
    bucket_object = ""
    file_path = ""
    file = ""
    # upload file
    # load file from udf
    # assert loaded file = orig file
    # cleanup

def test_load_file_to_file(pyexasol_connection):
    bucket_object = ""
    file_path = ""
    file = ""
    # upload file
    # load file from udf
    # assert loaded file = orig file
    # cleanup

def test_load_file_to_object_via_joblib(pyexasol_connection):
    bucket_object = ""
    file_path = ""
    file = ""
    # upload file
    # load file from udf
    # assert loaded file = orig file
    # cleanup
