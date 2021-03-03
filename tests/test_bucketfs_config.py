import pytest

from exasol_bucketfs_utils_python.bucketfs_config import BucketFSConnectionConfig, BucketFSConfig, BucketConfig


def test_bucketfs_connection_config_with_read_user():
    host = "localhost"
    port = 6666
    user = "r"
    pwd = "read"
    is_https = False
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    assert connection_config.host == host and \
           connection_config.port == port and \
           connection_config.user == user and \
           connection_config.pwd == pwd and \
           connection_config.is_https == is_https


def test_bucketfs_connection_config_with_write_user():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = False
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    assert connection_config.host == host and \
           connection_config.port == port and \
           connection_config.user == user and \
           connection_config.pwd == pwd and \
           connection_config.is_https == is_https


def test_bucketfs_connection_config_with_https():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    assert connection_config.host == host and \
           connection_config.port == port and \
           connection_config.user == user and \
           connection_config.pwd == pwd and \
           connection_config.is_https == is_https


def test_bucketfs_connection_config_set_https():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    with pytest.raises(AttributeError):
        connection_config.is_https = False


def test_bucketfs_connection_config_set_host():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    with pytest.raises(AttributeError):
        connection_config.host = "testhost"


def test_bucketfs_connection_config_set_port():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    with pytest.raises(AttributeError):
        connection_config.port = 7777


def test_bucketfs_connection_config_set_user():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    with pytest.raises(AttributeError):
        connection_config.user = "r"


def test_bucketfs_connection_config_set_pwd():
    host = "localhost"
    port = 6666
    user = "w"
    pwd = "write"
    is_https = True
    connection_config = BucketFSConnectionConfig(host=host, port=port, user=user, pwd=pwd,
                                                 is_https=is_https)
    with pytest.raises(AttributeError):
        connection_config.pwd = "abc"


def test_bucketfs_connection_config_with_not_allowed_user():
    with pytest.raises(ValueError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="abc", pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_empty_host():
    with pytest.raises(ValueError):
        connection_config = BucketFSConnectionConfig(host="", port=6666, user="w", pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_empty_user():
    with pytest.raises(ValueError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="", pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_empty_password():
    with pytest.raises(ValueError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="",
                                                     is_https=False)


def test_bucketfs_connection_config_with_none_as_host():
    with pytest.raises(TypeError):
        connection_config = BucketFSConnectionConfig(host=None, port=6666, user="w", pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_none_as_port():
    with pytest.raises(TypeError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=None, user="w", pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_none_as_user():
    with pytest.raises(TypeError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user=None, pwd="write",
                                                     is_https=False)


def test_bucketfs_connection_config_with_none_as_password():
    with pytest.raises(TypeError):
        connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd=None,
                                                     is_https=False)


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


def test_bucket_config_with_bucketfs_config():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_config = BucketFSConfig(bucketfs_name="bfsdefault", connection_config=connection_config)

    bucket_name = "default"
    bucket_config = BucketConfig(bucket_name=bucket_name, bucketfs_config=bucketfs_config)

    assert bucket_config.bucket_name == bucket_name and \
           bucket_config.bucketfs_config == bucketfs_config


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


def test_bucket_config_with_empty_bucket_name():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_config = BucketFSConfig(bucketfs_name="bfsdefault", connection_config=connection_config)

    with pytest.raises(ValueError):
        bucket_config = BucketConfig(bucket_name="", bucketfs_config=bucketfs_config)


def test_bucket_config_set_bucket_name():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_config = BucketFSConfig(bucketfs_name="bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)

    with pytest.raises(AttributeError):
        bucket_config.bucket_name = "test"


def test_bucket_config_set_bucketfs_config():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_config = BucketFSConfig(bucketfs_name="bfsdefault", connection_config=connection_config)
    bucket_config = BucketConfig(bucket_name="default", bucketfs_config=bucketfs_config)

    with pytest.raises(AttributeError):
        bucket_config.bucketfs_config = bucketfs_config


def test_bucket_config_with_empty_bucketfs_config():
    with pytest.raises(TypeError):
        bucket_config = BucketConfig(bucket_name="", bucketfs_config=None)


def test_bucket_config_with_None_as_bucket_name():
    connection_config = BucketFSConnectionConfig(host="localhost", port=6666, user="w", pwd="write",
                                                 is_https=False)

    bucketfs_config = BucketFSConfig(bucketfs_name="bfsdefault", connection_config=connection_config)

    with pytest.raises(TypeError):
        bucket_config = BucketConfig(bucket_name=None, bucketfs_config=bucketfs_config)
