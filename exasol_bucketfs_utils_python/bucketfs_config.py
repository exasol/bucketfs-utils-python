class BucketFSCredentials:
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd


class BucketFsConfig:
    def __init__(self, credentials: BucketFSCredentials, bucket, bucketfs_name, is_https=False):
        self.is_https = is_https
        self.credentials = credentials
        self.bucket = bucket
        self.bucketfs_name = bucketfs_name