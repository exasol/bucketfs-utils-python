import typing
from pathlib import Path
from tempfile import NamedTemporaryFile

import joblib
import requests

from exasol_bucketfs_utils_python import bucketfs_utils
from exasol_bucketfs_utils_python.bucketfs_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucket_http_url


def download_from_bucketfs_to_file(bucket_config: BucketConfig, bucket_file_path: str, local_file_path: Path):
    with local_file_path.open("wb") as f:
        download_from_bucketfs_to_fileobj(bucket_config, bucket_file_path, f)


def download_from_bucketfs_to_fileobj(bucket_config: BucketConfig, bucket_file_path: str, fileobj: typing.IO):
    if bucket_file_path is None:
        raise ValueError("bucket_file_path can't be None")
    url = generate_bucket_http_url(bucket_config, bucket_file_path)
    auth = bucketfs_utils.create_auth_object(bucket_config)
    with requests.get(url.geturl(), stream=True, auth=auth) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            fileobj.write(chunk)


def download_from_bucketfs_to_string(bucket_config: BucketConfig, bucket_file_path: str) -> str:
    if bucket_file_path is None:
        raise ValueError("bucket_file_path can't be None")
    url = generate_bucket_http_url(bucket_config, bucket_file_path)
    auth = bucketfs_utils.create_auth_object(bucket_config)
    response = requests.get(url.geturl(), auth=auth)
    response.raise_for_status()
    return response.text


def download_object_from_bucketfs_via_joblib(bucket_config: BucketConfig, bucket_file_path: str):
    with NamedTemporaryFile() as temp_file:
        download_from_bucketfs_to_fileobj(bucket_config, bucket_file_path, temp_file)
        temp_file.flush()
        temp_file.seek(0)
        obj = joblib.load(temp_file)
        return obj
