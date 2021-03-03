from typing import Union

from typeguard import typechecked


class BucketFSConnectionConfig:
    """
    The BucketFSConnectionConfig contains all necessary information
    to connect to the BucketFS Server via HTTP[s]
    """

    @typechecked(always=True)
    def __init__(self, host: str, port: int, user: str, pwd: str, is_https=False):
        self._is_https = is_https
        if host == "":
            raise ValueError("Host can't be an empty string")
        self._host = host
        self._port = port
        if user not in ["w", "r"]:  # The BucketFs currently supports only these two users
            raise ValueError(f"User can only be, 'w' (read-write access) or 'r' (read-only access), but got {user}")
        self._user = user
        if pwd == "":
            raise ValueError("Password can't be an empty string")
        self._pwd = pwd

    @property
    def is_https(self) -> bool:
        return self._is_https

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def user(self) -> str:
        return self._user

    @property
    def pwd(self) -> str:
        return self._pwd


class BucketFSConfig:
    """
    The BucketFSConfig contains all required information
    to access it either via HTTP[S] or in the file system inside of UDFs.
    The BucketFSConnectionConfig is here by optional,
    because in UDF we sometimes don't want to use HTTP[S].
    """

    @typechecked(always=True)
    def __init__(self, bucketfs_name: str, connection_config: Union[BucketFSConnectionConfig, None] = None):
        self._connection_config = connection_config
        if bucketfs_name == "":
            raise ValueError("BucketFS name can't be an empty string")
        self._bucketfs_name = bucketfs_name

    @property
    def bucketfs_name(self) -> str:
        return self._bucketfs_name

    @property
    def connection_config(self) -> Union[BucketFSConnectionConfig, None]:
        return self._connection_config


class BucketConfig:
    """
    The BucketConfig contains all required information about a BucketFS
    to access it either via HTTP[S] or in the file system inside of UDFs.
    """

    @typechecked(always=True)
    def __init__(self, bucket_name: str, bucketfs_config: BucketFSConfig):
        if bucket_name == "":
            raise ValueError("Bucket name can't be an empty string")
        self._bucket_name = bucket_name
        self._bucketfs_config = bucketfs_config

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def bucketfs_config(self) -> BucketFSConfig:
        return self._bucketfs_config
