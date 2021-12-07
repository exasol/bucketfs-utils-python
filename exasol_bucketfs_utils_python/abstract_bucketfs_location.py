import typing
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path


class AbstractBucketFSLocation(ABC):
    """
    Abstract class for a BucketFSLocation for uploading and downloading strings, fileobjects and joblib objects.
    Also able to read files from the BucketFS directly, if called from inside a UDF.
    """
    @abstractmethod
    def download_from_bucketfs_to_string(self, bucket_file_path: str) -> str:
        pass

    @abstractmethod
    def download_object_from_bucketfs_via_joblib(self, bucket_file_path: str) -> Any:
        pass

    @abstractmethod
    def upload_string_to_bucketfs(self, bucket_file_path: str, string: str):
        pass

    @abstractmethod
    def upload_object_to_bucketfs_via_joblib(self, object: Any,
                                             bucket_file_path: str,
                                             **kwargs):
        pass

    @abstractmethod
    def upload_fileobj_to_bucketfs(self,
                                   fileobj: typing.IO,
                                   bucket_file_path: str):
        pass

    # TODO add missing upload/download functions

    @abstractmethod
    def read_file_from_bucketfs_to_string(self, bucket_file_path: str) -> str:
        pass

    @abstractmethod
    def read_file_from_bucketfs_to_file(self, bucket_file_path: str, local_file_path: Path):
        pass

    @abstractmethod
    def read_file_from_bucketfs_to_fileobj(self, bucket_file_path: str, fileobj: typing.IO):
        pass

    @abstractmethod
    def read_file_from_bucketfs_via_joblib(self, bucket_file_path: str) -> typing.Any:
        pass
