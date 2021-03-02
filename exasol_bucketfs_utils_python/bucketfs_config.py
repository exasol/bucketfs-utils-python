from typing import Union


class BucketFSConnectionConfig:
    def __init__(self, host: str, port: str, user: str, pwd: str, is_https=False):
        self.is_https = is_https
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd


class BucketFsConfig:
    def __init__(self, bucketfs_name: str, connection_config: Union[BucketFSConnectionConfig, None] = None):
        self.connection_config = connection_config
        self.bucketfs_name = bucketfs_name


class BucketConfig:
    def __init__(self, bucket_name: str, bucketfs_config: BucketFsConfig):
        if bucketfs_config is None:
            raise TypeError("bucketfs_config can't be None")
        self.bucket_name = bucket_name
        self.bucketfs_config = bucketfs_config
