from exasol_bucketfs_utils_python.bucketfs_config import BucketFsConfig


def get_bucketfs_udf_path(bucketfs_config: BucketFsConfig, file_name: str):
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
    if bucketfs_config.is_https:
        protocol = "https"
    else:
        protocol = "http"
    url = f"{protocol}://{credentials}" \
          f"{bucketfs_config.credentials.host}:{bucketfs_config.credentials.port}/{bucketfs_config.bucket}/"
    if file_name is not None:
        url += f"{file_name}"
    return url