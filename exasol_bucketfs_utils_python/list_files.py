import requests
from pathlib import Path
from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python import bucketfs_utils
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucket_http_url


def list_files_in_bucketfs(bucket_config: BucketConfig,
                           bucket_file_path: str = "") -> str:
    """
    List files at the specified path in the bucket in BucketFs, line by line.

    :param bucket_config: BucketConfig for the bucket to download from
    :param bucket_file_path: Path in the bucket to download the file from
    :return: The list of the files in the BucketFS as string.
    """
    if bucket_file_path is None:
        raise ValueError("bucket_file_path can't be None")
    url = generate_bucket_http_url(bucket_config, "")
    auth = bucketfs_utils.create_auth_object(bucket_config)
    response = requests.get(url.geturl(), auth=auth)
    response.raise_for_status()

    bucket_file_path_parts = Path(bucket_file_path).parts
    files = []
    for path in response.text.split():
        path_parts = Path(path).parts
        if path_parts[:len(bucket_file_path_parts)] == bucket_file_path_parts:
            files.append(str(Path(*path_parts[len(bucket_file_path_parts):])))

    return "\n".join(files)


from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig
connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write", is_https=False)
bucketfs_config = BucketFSConfig(connection_config=connection_config, bucketfs_name="bfsdefault")
bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)

print(not list_files_in_bucketfs(bucket_config, "path/in/bucket/file.txt"))