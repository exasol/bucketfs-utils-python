import typing
from pathlib import PurePosixPath
from typing import Any

from exasol_bucketfs_utils_python import download, upload
from exasol_bucketfs_utils_python.bucket_config import BucketConfig

from exasol_bucketfs_utils_python.abstract_bucketfs_location import AbstractBucketFSLocation


class BucketFSLocation(AbstractBucketFSLocation):

    def __init__(self, bucket_config: BucketConfig, base_path: PurePosixPath):
        self.base_path = base_path
        self.bucket_config = bucket_config

    def get_complete_file_path_in_bucket(self, bucket_file_path) -> str:
        return str(PurePosixPath(self.base_path, bucket_file_path))

    def download_from_bucketfs_to_string(self, bucket_file_path: str) -> str:
        result = download.download_from_bucketfs_to_string(
            self.bucket_config,
            self.get_complete_file_path_in_bucket(bucket_file_path))
        return result

    def download_object_from_bucketfs_via_joblib(self, bucket_file_path: str) -> Any:
        result = download.download_object_from_bucketfs_via_joblib(
            self.bucket_config,
            self.get_complete_file_path_in_bucket(bucket_file_path))
        return result

    def upload_string_to_bucketfs(self, bucket_file_path: str, string: str):
        result = upload.upload_string_to_bucketfs(
            self.bucket_config,
            self.get_complete_file_path_in_bucket(bucket_file_path),
            string)
        return result

    def upload_object_to_bucketfs_via_joblib(self, object: Any,
                                             bucket_file_path: str,
                                             **kwargs):
        result = upload.upload_object_to_bucketfs_via_joblib(
            object,
            self.bucket_config,
            self.get_complete_file_path_in_bucket(bucket_file_path),
            **kwargs)
        return result

    def upload_fileobj_to_bucketfs(self,
                                   fileobj: typing.IO,
                                   bucket_file_path: str):
        result = upload.upload_fileobj_to_bucketfs(
            self.bucket_config,
            self.get_complete_file_path_in_bucket(bucket_file_path),
            fileobj)
        return result
