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
