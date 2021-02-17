import os
import typing
from pathlib import Path
from tempfile import NamedTemporaryFile

import joblib
import requests

from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig
from exasol_bucketfs_utils_python.bucketfs_udf_utils import generate_bucketfs_url, get_bucketfs_udf_path


def upload_file_to_bucketfs(bucketfs_config: BucketFsConfig, bucket_file_path: str, local_file_path: Path):
    with local_file_path.open("rb") as f:
        upload_fileobj_to_bucketfs(bucketfs_config, bucket_file_path, f)


def upload_fileobj_to_bucketfs(bucketfs_config: BucketFsConfig, bucket_file_path: str, fileobj: typing.IO):
    url = generate_bucketfs_url(bucketfs_config, bucket_file_path)
    response = requests.put(url, data=fileobj)
    response.raise_for_status()
    path = get_bucketfs_udf_path(bucketfs_config, bucket_file_path)
    return url, path


def upload_string_to_bucketfs(bucketfs_config: BucketFsConfig, bucket_file_path: str, string: str):
    url = generate_bucketfs_url(bucketfs_config, bucket_file_path)
    response = requests.put(url, data=string.encode("UTF-8"))
    response.raise_for_status()
    path = get_bucketfs_udf_path(bucketfs_config, bucket_file_path)
    return url, path


def upload_object_to_bucketfs_via_joblib(object, bucketfs_config: BucketFsConfig, bucket_file_path: str, compress=True):
    with NamedTemporaryFile() as temp_file:
        joblib.dump(object, temp_file.name, compress=compress)
        temp_file.flush()
        temp_file.seek(0)
        upload_fileobj_to_bucketfs(bucketfs_config, bucket_file_path, temp_file)
