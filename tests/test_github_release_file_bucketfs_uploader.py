import requests

from extension_downloading.github_release_file_bucketfs_uploader import GithubReleaseFileBucketFSUploader
from tests.bucketfs_utils import BucketFsConfig, generate_bucketfs_url, BucketFSCredentials


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
    bucketfs_config = BucketFsConfig(BucketFSCredentials())
    upload_file_to_bucket(bucketfs_config)
    response = requests.get("http://{}:{}/default/virtualschemas/".format(bucketfs_config.credentials.host,
                                                   bucketfs_config.credentials.port))
    print(response.text)
    assert "virtual-schema-dist" in response.text
