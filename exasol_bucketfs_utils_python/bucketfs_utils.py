from typing import Union

from requests.auth import HTTPBasicAuth

from exasol_bucketfs_utils_python.bucketfs_config import BucketConfig, BucketFsConfig

ARCHIVE_EXTENSIONS = [".tar.gz", ".tar.bz2", ".zip", ".tar"]


def _correct_path_in_bucket_for_archives(path_in_bucket: str) -> str:
    for extension in ARCHIVE_EXTENSIONS:
        if path_in_bucket.endswith(extension):
            path_in_bucket = path_in_bucket[:-len(extension)]
            break
    return path_in_bucket


def get_bucketfs_udf_path(bucketfs_config: BucketFsConfig) -> str:
    """
    This function generates the path where UDFs can access the content of a BucketFS in there file system
    :param bucketfs_config: Config of the BucketFS, the BucketFSConnectionConfig in the BucketFSConfig can None
    :return: Path of the given BucketFS in the file system of UDFs
    """
    path = f"/buckets/{bucketfs_config.bucketfs_name}"
    return path


def get_bucket_udf_path(bucket_config: BucketConfig, path_in_bucket: Union[None, str]) -> str:
    """
    This function generates the path where UDFs can access the content of a Bucket or
    the given Path in a Bucket in there file system
    :param bucket_config: Config of the Bucket, the BucketFSConnectionConfig in the BucketFSConfig can be None
    :param path_in_bucket: If not None, path_in_bucket gets concatenated to the path of the bucket
    :return:
    """
    bucketfs_path = get_bucketfs_udf_path(bucket_config.bucketfs_config)
    path = f"{bucketfs_path}/{bucket_config.bucket_name}"

    if path_in_bucket is not None:
        path_in_bucket = _correct_path_in_bucket_for_archives(path_in_bucket)
        if path_in_bucket.startswith("/"):
            path_in_bucket = path_in_bucket[1:]
        path = f"{path}/{path_in_bucket}"
    return path


def generate_bucketfs_url(bucketfs_config: BucketFsConfig, with_credentials: bool = False) -> str:
    if bucketfs_config.connection_config is None:
        raise TypeError("bucket_config.bucketfs_config.connection_config can't be None for this operations")
    if with_credentials:
        credentials = f"{bucketfs_config.connection_config.user}:{bucketfs_config.connection_config.pwd}@"
    else:
        credentials = ""
    if bucketfs_config.connection_config.is_https:
        protocol = "https"
    else:
        protocol = "http"
    url = f"{protocol}://{credentials}" \
          f"{bucketfs_config.connection_config.host}:{bucketfs_config.connection_config.port}"
    return url


def generate_bucket_url(bucket_config: BucketConfig, path_in_bucket: Union[None, str], with_credentials: bool = False):
    url = generate_bucketfs_url(bucket_config.bucketfs_config, with_credentials)
    url = url + f"/{bucket_config.bucket_name}"
    if path_in_bucket is not None:
        if path_in_bucket.startswith("/"):
            path_in_bucket = path_in_bucket[1:]
        url += f"/{path_in_bucket}"
    return url


def create_auth_object(bucket_config):
    if bucket_config.bucketfs_config.connection_config is None:
        raise TypeError("bucket_config.bucketfs_config.connection_config can't be None for this operations")
    auth = HTTPBasicAuth(
        bucket_config.bucketfs_config.connection_config.user,
        bucket_config.bucketfs_config.connection_config.pwd)
    return auth
