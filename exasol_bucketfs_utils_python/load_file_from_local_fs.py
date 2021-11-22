from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucket_udf_path
import typing
from pathlib import Path
from tempfile import NamedTemporaryFile
import joblib
# TODO remove class

class LoadFromLocalFS:
    """

    """
    #CONNECTION_NAME = "tensorflow_config"

    def read_file_from_bucketfs_to_string(self, ctx, exa, bucket_config: BucketConfig) -> str:
        """

        """
        bucket_file_path = ctx.path
        if bucket_file_path is None:
            raise ValueError("bucket_file_path can't be None")
        bucket_path = generate_bucket_udf_path(bucket_config, bucket_file_path)
        text_as_string = open(bucket_path).read()
        return text_as_string

    def read_file_from_bucketfs_to_file(self, ctx, exa, bucket_config: BucketConfig, local_file_path: Path):
        """

        """
        with local_file_path.open("wb") as f:
            self.read_file_from_bucketfs_to_fileobj(ctx, exa, bucket_config, fileobj=f)

    def read_file_from_bucketfs_to_fileobj(self, ctx, exa, bucket_config: BucketConfig, fileobj: typing.IO):
        """

        """
        bucket_file_path = ctx.path
        if bucket_file_path is None:
            raise ValueError("bucket_file_path can't be None")
        bucket_path = generate_bucket_udf_path(bucket_config, bucket_file_path)
        with open(bucket_path, "rb") as file:
            file.seek(0)
            fileobj.write(file.read())

    def read_file_from_bucketfs_via_joblib(self, ctx, exa, bucket_config: BucketConfig) -> typing.Any:
        """

        """
        with NamedTemporaryFile() as temp_file:
            self.read_file_from_bucketfs_to_fileobj(ctx, exa, bucket_config, temp_file)
            temp_file.flush()
            temp_file.seek(0)
            obj = joblib.load(temp_file)
            return obj
