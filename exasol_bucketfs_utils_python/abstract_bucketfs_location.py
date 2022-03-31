from abc import ABC, abstractmethod
from typing import Any, Tuple, IO
from pathlib import PurePosixPath, Path
from urllib.parse import ParseResult


class AbstractBucketFSLocation(ABC):
    """
    Abstract class for a BucketFSLocation for uploading and downloading strings,
    fileobjects and joblib objects. Also able to read files from the BucketFS
    directly, if called from inside a UDF.
    """
    @abstractmethod
    def download_from_bucketfs_to_string(self,
                                         bucket_file_path: str) -> str:
        pass

    @abstractmethod
    def download_object_from_bucketfs_via_joblib(self,
                                                 bucket_file_path: str) -> Any:
        pass

    @abstractmethod
    def upload_string_to_bucketfs(self,
                                  bucket_file_path: str,
                                  string: str) -> \
            Tuple[ParseResult, PurePosixPath]:
        pass

    @abstractmethod
    def upload_object_to_bucketfs_via_joblib(self,
                                             object: Any,
                                             bucket_file_path: str,
                                             **kwargs) -> \
            Tuple[ParseResult, PurePosixPath]:
        pass

    @abstractmethod
    def upload_fileobj_to_bucketfs(self,
                                   fileobj: IO,
                                   bucket_file_path: str) -> \
            Tuple[ParseResult, PurePosixPath]:
        pass

    # TODO add missing upload/download functions

    @abstractmethod
    def read_file_from_bucketfs_to_string(self,
                                          bucket_file_path: str) -> str:
        pass

    @abstractmethod
    def read_file_from_bucketfs_to_file(self,
                                        bucket_file_path: str,
                                        local_file_path: Path) -> None:
        pass

    @abstractmethod
    def read_file_from_bucketfs_to_fileobj(self,
                                           bucket_file_path: str,
                                           fileobj: IO) -> None:
        pass

    @abstractmethod
    def read_file_from_bucketfs_via_joblib(self,
                                           bucket_file_path: str) -> Any:
        pass

    @abstractmethod
    def list_files_in_bucketfs(self,
                               bucket_file_path: str) -> str:
        pass