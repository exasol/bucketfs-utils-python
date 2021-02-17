import typing
from pathlib import Path
from tempfile import NamedTemporaryFile

import joblib
import requests
from requests.auth import HTTPBasicAuth

from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucketfs_url


def download_from_bucketfs_to_file(bucketfs_config: BucketFsConfig, bucket_file_path: str, local_file_path: Path):
    with local_file_path.open("wb") as f:
        download_from_bucketfs_to_fileobj(bucketfs_config, bucket_file_path, f)


def download_from_bucketfs_to_fileobj(bucketfs_config: BucketFsConfig, bucket_file_path: str, fileobj: typing.IO):
    url = generate_bucketfs_url(bucketfs_config, bucket_file_path)
    auth = HTTPBasicAuth(
        bucketfs_config.credentials.user,
        bucketfs_config.credentials.pwd)
    with requests.get(url, stream=True, auth=auth) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            fileobj.write(chunk)


def download_from_bucketfs_to_string(bucketfs_config: BucketFsConfig, bucket_file_path: str) -> str:
    url = generate_bucketfs_url(bucketfs_config, bucket_file_path)
    auth = HTTPBasicAuth(
        bucketfs_config.credentials.user,
        bucketfs_config.credentials.pwd)
    response = requests.get(url,auth=auth)
    response.raise_for_status()
    return response.text


def download_object_from_bucketfs_via_joblib(object, bucketfs_config: BucketFsConfig, file_name: str, compress=True):
    with NamedTemporaryFile() as temp_file:
        download_from_bucketfs_to_fileobj(bucketfs_config, file_name, temp_file)
        temp_file.flush()
        temp_file.seek(0)
        object = joblib.load(temp_file)
        return object
