import typing
from abc import ABC, abstractmethod
from typing import Any


class AbstractBucketFSLocation(ABC):

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
