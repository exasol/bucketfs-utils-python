from typing import Union


class BucketFSConnectionConfig:
    """
    The BucketFSConnectionConfig contains all necessary information
    to connect to the BucketFS Server via HTTP[s]
    """
    def __init__(self, host: str, port: str, user: str, pwd: str, is_https=False):
        self.is_https = is_https
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd


class BucketFsConfig:
    """
    The BucketFSConfig contains all required information
    to access it either via HTTP[S] or in the file system inside of UDFs.
    The BucketFSConnectionConfig is here by optional,
    because in UDF we sometimes don't want to use HTTP[S].
    """
    def __init__(self, bucketfs_name: str, connection_config: Union[BucketFSConnectionConfig, None] = None):
        self.connection_config = connection_config
        self.bucketfs_name = bucketfs_name


class BucketConfig:
    """
    The BucketConfig contains all required information about a BucketFS
    to access it either via HTTP[S] or in the file system inside of UDFs.
    """
    def __init__(self, bucket_name: str, bucketfs_config: BucketFsConfig):
        if bucketfs_config is None:
            raise TypeError("bucketfs_config can't be None")
        self.bucket_name = bucket_name
        self.bucketfs_config = bucketfs_config
