from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig


def get_bucketfs_udf_path(bucketfs_config: BucketFsConfig, path_in_bucket: str):
    archive_extensions = [".tar.gz", ".tar.bz2", ".zip", ".tar"]
    path_prefix = ""
    for extension in archive_extensions:
        if path_in_bucket.endswith(extension):
            path_in_bucket = path_in_bucket[:-len(extension)]
            path_prefix = "/"
            break
    if path_in_bucket.startswith("/"):
        path_in_bucket = path_in_bucket[1:]
    path = f"/buckets/{bucketfs_config.bucketfs_name}/{bucketfs_config.bucket}/{path_in_bucket}{path_prefix}"
    return path


def generate_bucketfs_url(bucketfs_config: BucketFsConfig, path_in_bucket: str, with_credentials: bool = False):
    if with_credentials:
        credentials = f"{bucketfs_config.credentials.user}:{bucketfs_config.credentials.pwd}@"
    else:
        credentials = ""
    if bucketfs_config.is_https:
        protocol = "https"
    else:
        protocol = "http"
    url = f"{protocol}://{credentials}" \
          f"{bucketfs_config.credentials.host}:{bucketfs_config.credentials.port}/{bucketfs_config.bucket}/"
    if path_in_bucket is not None:
        if path_in_bucket.startswith("/"):
            path_in_bucket = path_in_bucket[1:]
        url += f"{path_in_bucket}"
    return url