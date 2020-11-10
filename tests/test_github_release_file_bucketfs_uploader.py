import requests

from extension_downloading.github_release_file_bucketfs_uploader import GithubReleaseFileBucketFSUploader
from tests.bucketfs_utils import BucketFsConfig, generate_bucketfs_url, BucketFSCredentials


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


def test_uploading_github_release_to_bucketfs():
    database_config = DatabaseConfig(DatabaseCredentials(), "test_schema")
    bucketfs_config = BucketFsConfig(BucketFSCredentials())
    upload_file_to_bucket(bucketfs_config)
    response = requests.get("http://{}:{}/virtualschemas/".format(database_config.credentials.host,
                                                                  database_config.credentials.port))
    assert "virtual-schema-dist" in response.text
