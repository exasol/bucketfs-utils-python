import os
import uuid
from pathlib import Path

import requests
import joblib

from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig
from exasol_bucketfs_utils_python.bucketfs_udf_utils import generate_bucketfs_url


def download_from_bucketfs_to_file(bucketfs_config: BucketFsConfig, file_name: str, file_path: Path):
    url = generate_bucketfs_url(bucketfs_config, file_name)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with file_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def download_from_bucketfs_to_string(bucketfs_config: BucketFsConfig, file_name: str)->str:
    url = generate_bucketfs_url(bucketfs_config, file_name)
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def download_object_from_bucketfs_via_joblib(object, bucketfs_config: BucketFsConfig, file_name: str, compress=True):
    temp_file = Path("/tmp/" + str(uuid.uuid4().hex + ".pkl"))
    try:
        joblib.dump(object, str(temp_file), compress=compress)
        download_from_bucketfs_to_file(bucketfs_config, file_name, temp_file)
        object = joblib.load(temp_file)
        return object
    finally:
        try:
            os.remove(temp_file)
        except OSError:
            pass