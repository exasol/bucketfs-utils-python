from typing import Union


class BucketFSConnectionConfig:
    """
    The BucketFSConnectionConfig contains all necessary information
    to connect to the BucketFS Server via HTTP[s]
    """

    def __init__(self, host: str, port: int, user: str, pwd: str, is_https=False):
        self.is_https = is_https
        if host == "":
            raise ValueError("Host can't be an empty string")
        self.host = host
        self.port = port
        if user not in ["w", "r"]:  # The BucketFs currently supports only these two users
            raise ValueError(f"User can only be, 'w' (read-write access) or 'r' (read-only access), but got {user}")
        self.user = user
        if pwd == "":
            raise ValueError("Password can't be an empty string")
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
        if bucketfs_name == "":
            raise ValueError("BucketFS name can't be an empty string")
        self.bucketfs_name = bucketfs_name


class BucketConfig:
    """
    The BucketConfig contains all required information about a BucketFS
    to access it either via HTTP[S] or in the file system inside of UDFs.
    """

    def __init__(self, bucket_name: str, bucketfs_config: BucketFsConfig):
        if bucketfs_config is None:
            raise TypeError("bucketfs_config can't be None")
        if bucket_name == "":
            raise ValueError("Bucket name can't be an empty string")
        self.bucket_name = bucket_name
        self.bucketfs_config = bucketfs_config
