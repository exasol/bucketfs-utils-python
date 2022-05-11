from typing import Any, IO
from pathlib import PurePosixPath, Path
from typing import Any
import joblib
from exasol_bucketfs_utils_python.abstract_bucketfs_location import \
    AbstractBucketFSLocation


class LocalFSMockBucketFSLocation(AbstractBucketFSLocation):
    """
    LocalFSMockBucketFSLocation implements AbstractBucketFSLocation.
    Mockup for use/testing of the BucketFSLocation for a local File System.
    Used to upload fileobjects, strings or joblib objects to the LocalFS given a path and the object,
    or to download or read objects into strings, fileobjects or joblib objects from the LocalFS given a file path.
    """

    def __init__(self, base_path: PurePosixPath):
        self.base_path = base_path

    def get_complete_file_path_in_bucket(self, bucket_file_path) -> str:
        return str(PurePosixPath(self.base_path, bucket_file_path))

    def download_from_bucketfs_to_string(self, bucket_file_path: str) -> str:
        with open(self.get_complete_file_path_in_bucket(
                bucket_file_path), "rt") as f:
            result = f.read()
            return result

    def download_object_from_bucketfs_via_joblib(self,
                                                 bucket_file_path: str) -> Any:
        result = joblib.load(
            self.get_complete_file_path_in_bucket(bucket_file_path))
        return result

    def upload_string_to_bucketfs(self,
                                  bucket_file_path: str,
                                  string: str) -> None:
        path = self.get_complete_file_path_in_bucket(bucket_file_path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wt") as f:
            f.write(string)

    def upload_object_to_bucketfs_via_joblib(self,
                                             object_: Any,
                                             bucket_file_path: str,
                                             **kwargs) -> None:
        path = self.get_complete_file_path_in_bucket(bucket_file_path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(object_, path, **kwargs)

    def upload_fileobj_to_bucketfs(self,
                                   fileobj: IO,
                                   bucket_file_path: str) -> None:
        path = self.get_complete_file_path_in_bucket(bucket_file_path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            for chunk in iter(lambda: fileobj.read(10000), b''):
                f.write(chunk)

    def read_file_from_bucketfs_to_fileobj(self,
                                           bucket_file_path: str,
                                           fileobj: IO) -> None:
        bucket_path = self.get_complete_file_path_in_bucket(bucket_file_path)
        with open(bucket_path, "rb") as read_file:
            read_file.seek(0)
            fileobj.write(read_file.read())

    def read_file_from_bucketfs_to_file(self,
                                        bucket_file_path: str,
                                        local_file_path: Path) -> None:
        with open(local_file_path, "wb") as fileobj:
            self.read_file_from_bucketfs_to_fileobj(bucket_file_path, fileobj)

    def read_file_from_bucketfs_to_string(self,
                                          bucket_file_path: str) -> str:
        result = self.download_from_bucketfs_to_string(bucket_file_path)
        return result

    def read_file_from_bucketfs_via_joblib(self,
                                           bucket_file_path: str) -> Any:
        result = joblib.load(
            self.get_complete_file_path_in_bucket(bucket_file_path))
        return result

    def list_files_in_bucketfs(self,
                               bucket_file_path: str) -> list:
        path = self.get_complete_file_path_in_bucket(bucket_file_path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        return ["."]

    def delete_file_in_bucketfs(
            self,
            bucket_file_path: str) -> None:
        path = self.get_complete_file_path_in_bucket(bucket_file_path)
        Path(path).unlink(missing_ok=True)
