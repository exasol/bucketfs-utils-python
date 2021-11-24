import typing
from pathlib import PurePosixPath, Path
from typing import Any

from exasol_bucketfs_utils_python import download, upload
from exasol_bucketfs_utils_python import load_file_from_local_fs as from_BFS
from exasol_bucketfs_utils_python.bucket_config import BucketConfig

from exasol_bucketfs_utils_python.abstract_bucketfs_location import AbstractBucketFSLocation

class BucketFSLocation(AbstractBucketFSLocation):
    """
    BucketFSLocation implements AbstractBucketFSLocation.
    BucketFSLocation is used to upload fileobjects, strings or joblib objects to the BucketFS given a path and the object,
    or to download objects into strings, fileobjects or joblib objects from the BucketFS given a file path.
    Also able to read files from the BucketFS directly, if called from inside a UDF.
    """

    def __init__(self, bucket_config: BucketConfig, base_path: PurePosixPath):
        self.base_path = base_path
        self.bucket_config = bucket_config

    def get_complete_file_path_in_bucket(self, bucket_file_path: str) -> str:
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

    def read_file_from_bucketfs_to_string(self, bucket_file_path: str) -> str:
        result = from_BFS.read_file_from_bucketfs_to_string(
            bucket_file_path,
            self.bucket_config
        )
        return result

    def read_file_from_bucketfs_via_joblib(self, bucket_file_path: str) -> typing.Any:
        result = from_BFS.read_file_from_bucketfs_via_joblib(
            bucket_file_path,
            self.bucket_config
        )
        return result


    def read_file_from_bucketfs_to_file(self, bucket_file_path: str, local_file_path: Path):
        result = from_BFS.read_file_from_bucketfs_to_file(
            bucket_file_path,
            self.bucket_config,
            local_file_path
        )
        return result

    def read_file_from_bucketfs_to_fileobj(self, bucket_file_path: str, fileobj: typing.IO):
        result = from_BFS.read_file_from_bucketfs_to_fileobj(
            bucket_file_path,
            self.bucket_config,
            fileobj
        )
        return result
