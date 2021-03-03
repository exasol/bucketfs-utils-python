import pytest

from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConfig
from exasol_bucketfs_utils_python.bucketfs_connection_config import BucketFSConnectionConfig


def test_bucketfs_config_with_empty_bucketfs_name():
    with pytest.raises(ValueError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                     is_https=False)

        bucketfs_config = BucketFSConfig(bucketfs_name="", connection_config=connection_config)


def test_bucketfs_config_with_bucketfs_connection_config():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_name = "bfsdefault"
    bucketfs_config = BucketFSConfig(bucketfs_name=bucketfs_name, connection_config=connection_config)

    assert bucketfs_config.bucketfs_name == bucketfs_name and \
           bucketfs_config.connection_config == connection_config


def test_bucketfs_config_without_bucketfs_connection_config():
    bucketfs_name = "bfsdefault"
    bucketfs_config = BucketFSConfig(bucketfs_name=bucketfs_name)
    assert bucketfs_config.bucketfs_name == bucketfs_name and \
           bucketfs_config.connection_config == None


def test_bucketfs_config_with_none_as_bucketfs_name():
    with pytest.raises(TypeError):
        bucketfs_name = None
        bucketfs_config = BucketFSConfig(bucketfs_name=bucketfs_name)


def test_bucketfs_config_set_bucketfs_name():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_name = "bfsdefault"
    bucketfs_config = BucketFSConfig(bucketfs_name=bucketfs_name, connection_config=connection_config)

    with pytest.raises(AttributeError):
        bucketfs_config.bucketfs_name = "test"


def test_bucketfs_config_set_bucketfs_connection_config():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_name = "bfsdefault"
    bucketfs_config = BucketFSConfig(bucketfs_name=bucketfs_name, connection_config=connection_config)

    with pytest.raises(AttributeError):
        bucketfs_config.connection_config = None
