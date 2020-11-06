import os
import re
import subprocess
import textwrap
from pathlib import Path

import pyexasol

import extension_downloading

from extension_downloading.GithubReleaseFileBucketFSUploader import GithubReleaseFileBucketFSUploader
from tests.bucketfs_utils import BucketFsConfig, generate_bucketfs_url, upload_file_to_bucketfs, BucketFSCredentials


class DatabaseCredentials:
    def __init__(self, host="localhost", port=8888, user="sys", pwd="exasol"):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd


class DatabaseConfig:
    def __init__(self, credentials: DatabaseCredentials, schema: str):
        self.credentials = credentials
        self.schema = schema


def find_project_base_directory():
    return Path(extension_downloading.__file__).parent.parent


def upload_file_to_bucket(bucketfs_config):
    release_uploader = \
        GithubReleaseFileBucketFSUploader(file_to_download_name="virtual-schema-dist",
                                          github_user="exasol",
                                          repository_name="exasol-virtual-schema",
                                          release_name="latest",
                                          path_inside_bucket="virtualschemas/")
    release_uploader.upload(
        generate_bucketfs_url(bucketfs_config, file_name=None, with_credentials=False),
        username=bucketfs_config.credentials.user,
        password=bucketfs_config.credentials.pwd)


def upload_sdist(bucketfs_config: BucketFsConfig):
    result = subprocess.run(["echo $PATH; poetry build"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    result.check_returncode()
    project_base_directory = find_project_base_directory()
    dist_directory = Path(project_base_directory, "dist")
    tar_release_file_name = next(filter(lambda x: x.endswith(".tar.gz"), os.listdir(dist_directory)))
    tar_release_file_path = Path(dist_directory, tar_release_file_name)
    url, path = upload_file_to_bucketfs(bucketfs_config, tar_release_file_name, tar_release_file_path)
    return url, path


def prepare_test(con, database_config):
    bucketfs_config = BucketFsConfig(BucketFSCredentials())
    sdist_url, sdist_path = upload_sdist(bucketfs_config)
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {database_config.schema};")
    con.execute(f"OPEN SCHEMA {database_config.schema};")


def test_tensorflow_udf_train():
    database_config = DatabaseConfig(DatabaseCredentials(), "test_tensorflow_udf")
    bucketfs_config = BucketFsConfig(BucketFSCredentials())

    upload_file_to_bucket(bucketfs_config)
    with pyexasol.connect(
            dsn=f"{database_config.credentials.host}:{database_config.credentials.port}",
            user=database_config.credentials.user,
            password=database_config.credentials.pwd) as con:
        try:
            prepare_test(con, database_config)
            con.execute(textwrap.dedent(f"""
            CREATE OR REPLACE PYTHON SCALAR SCRIPT EXA_toolbox.bucketfs_ls(my_path VARCHAR(256)) 
            EMITS (files VARCHAR(256)) AS
            import subprocess

            def run(c):
                try:
                    p = subprocess.Popen('ls -F ' + c.my_path,
                                         stdout    = subprocess.PIPE,
                                         stderr    = subprocess.STDOUT,
                                         close_fds = True,
                                         shell     = True)
                    out, err = p.communicate()
                    for line in out.strip().split('\n'):
                        c.emit(line)
                finally:
                    if p is not None:
                        try: p.kill()
                        except: pass
            /
            """))
            result = con.execute("SELECT bucketfs_ls('/buckets/bfsdefault/default')").fetchall()
            output = result[0][0]
            print(output)
            assert re.match(
                r"""some text""",
                output)
        finally:
            con.execute(f"DROP SCHEMA IF EXISTS {database_config.schema} CASCADE;")
