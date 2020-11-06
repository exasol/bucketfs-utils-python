from pathlib import Path

import requests


class BucketFSCredentials:
    def __init__(self, host="localhost", port=6666, user="w", pwd="write"):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd


class BucketFsConfig:
    def __init__(self, credentials: BucketFSCredentials, bucket="default", bucketfs_name="bfsdefault"):
        self.credentials = credentials
        self.bucket = bucket
        self.bucketfs_name = bucketfs_name


def upload_file_to_bucketfs(bucket_config: BucketFsConfig, file_name: str, file_path: Path):
    with file_path.open("rb") as f:
        url = generate_bucketfs_url(bucket_config, file_name)
        response = requests.put(url, data=f)
        response.raise_for_status()
        path = get_bucketfs_path(bucket_config, file_name)
        return url, path


def upload_string_to_bucketfs(bucketfs_config: BucketFsConfig, file_name: str, string: str):
    url = generate_bucketfs_url(bucketfs_config, file_name)
    response = requests.put(url, data=string.encode("UTF-8"))
    response.raise_for_status()
    path = get_bucketfs_path(bucketfs_config, file_name)
    return url, path


def get_bucketfs_path(bucketfs_config: BucketFsConfig, file_name: str):
    archive_extensions = [".tar.gz", ".tar.bz2", ".zip", ".tar"]
    for extension in archive_extensions:
        if file_name.endswith(extension):
            file_name = file_name[:-len(extension)]
            break
    path = f"/buckets/{bucketfs_config.bucketfs_name}/{bucketfs_config.bucket}/{file_name}"
    return path


def generate_bucketfs_url(bucketfs_config: BucketFsConfig, file_name: str, with_credentials: bool = True):
    if with_credentials:
        credentials = f"{bucketfs_config.credentials.user}:{bucketfs_config.credentials.pwd}@"
    else:
        credentials = ""
    url = f"http://{credentials}" \
          f"{bucketfs_config.credentials.host}:{bucketfs_config.credentials.port}/{bucketfs_config.bucket}/"
    if file_name is not None:
        url += f"{file_name}"
    return url
