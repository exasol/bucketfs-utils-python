import typing
from pathlib import Path
from tempfile import NamedTemporaryFile

import joblib
import requests

from exasol_bucketfs_utils_python import bucketfs_utils
from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucket_http_url, generate_bucket_udf_path


def upload_file_to_bucketfs(bucket_config: BucketConfig, bucket_file_path: str, local_file_path: Path):
    with local_file_path.open("rb") as f:
        return upload_fileobj_to_bucketfs(bucket_config, bucket_file_path, f)


def upload_fileobj_to_bucketfs(bucket_config: BucketConfig, bucket_file_path: str, fileobj: typing.IO):
    if bucket_file_path is None:
        raise ValueError("bucket_file_path can't be None")
    url = generate_bucket_http_url(bucket_config, bucket_file_path)
    auth = bucketfs_utils.create_auth_object(bucket_config)
    response = requests.put(url.geturl(), data=fileobj, auth=auth)
    response.raise_for_status()
    path = generate_bucket_udf_path(bucket_config, bucket_file_path)
    return url, path


def upload_string_to_bucketfs(bucket_config: BucketConfig, bucket_file_path: str, string: str):
    if bucket_file_path is None:
        raise ValueError("bucket_file_path can't be None")
    url = generate_bucket_http_url(bucket_config, bucket_file_path)
    auth = bucketfs_utils.create_auth_object(bucket_config)
    response = requests.put(url.geturl(), data=string.encode("UTF-8"), auth=auth)
    response.raise_for_status()
    path = generate_bucket_udf_path(bucket_config, bucket_file_path)
    return url, path


def upload_object_to_bucketfs_via_joblib(object, bucket_config: BucketConfig, bucket_file_path: str, compress=True):
    with NamedTemporaryFile() as temp_file:
        joblib.dump(object, temp_file.name, compress=compress)
        temp_file.flush()
        temp_file.seek(0)
        upload_fileobj_to_bucketfs(bucket_config, bucket_file_path, temp_file)