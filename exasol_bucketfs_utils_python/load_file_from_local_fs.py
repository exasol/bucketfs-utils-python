from exasol_bucketfs_utils_python.bucket_config import BucketConfig
from exasol_bucketfs_utils_python.bucketfs_utils import generate_bucket_udf_path
import typing
from pathlib import Path
from tempfile import NamedTemporaryFile
import joblib

class LoadFromLocalFS:
    """
    Class for reading Files from the BucketFS inside a UDF.
    Can read into a String, a file given by path, a given FileObject and via joblib.
    """

    def read_file_from_bucketfs_to_string(self, ctx, exa, bucket_config: BucketConfig) -> str:
        """
        Read a file from the specified path in the bucket in the BucketFs into a string.
        Can be used inside a UDF.

        :param bucket_config: BucketConfig for the bucket to read from
        :param ctx: Context of the UDf. Path in the bucket to download the file from is read from this. #TODO Or do we want an extra param for this?
        :return: The content of the file in the BucketFS as string
        """
        bucket_file_path = ctx.path
        if bucket_file_path is None:
            raise ValueError("bucket_file_path can't be None")
        bucket_path = generate_bucket_udf_path(bucket_config, bucket_file_path)
        text_as_string = open(bucket_path).read()
        return text_as_string

    def read_file_from_bucketfs_to_file(self, ctx, exa, bucket_config: BucketConfig, local_file_path: Path):
        """
        Read a file from the specified path in the bucket in the BucketFs and save as a local file
        Can be used inside a UDF.

        :param bucket_config: BucketConfig for the bucket to download from
        :param local_file_path: Path in the bucket to download the file from
        :param ctx: Context of the UDf. Path in the bucket to download the file from is read from this. #TODO Or do we want an extra param for this? Possible remove ctx and exa here?
        :return: None
        """
        with local_file_path.open("wb") as f:
            self.read_file_from_bucketfs_to_fileobj(ctx, exa, bucket_config, fileobj=f)

    def read_file_from_bucketfs_to_fileobj(self, ctx, exa, bucket_config: BucketConfig, fileobj: typing.IO):
        """
        Download a file from the specified path in the bucket in the BucketFs into a given
        `file object <https://docs.python.org/3/glossary.html#term-file-object>`_
        Can be used inside a UDF.

        :param bucket_config: BucketConfig for the bucket to download from
        :param ctx: Context of the UDf. Path in the bucket to download the file from is read from this. #TODO Or do we want an extra param for this? Possible remove ctx and exa here?
        :param fileobj: File object where the data of the file in the BucketFS is downloaded to
        :return: None
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
        Download a file from the specified path in the bucket in the BucketFs and deserialize it via
        `joblib.load <https://joblib.readthedocs.io/en/latest/generated/joblib.load.html#>`_
        Can be used inside a UDF.

        :param bucket_config: BucketConfig for the bucket to download from
        :param ctx: Context of the UDf. Path in the bucket to download the file from is read from this. #TODO Or do we want an extra param for this? Possible remove ctx and exa here?
        :return: The deserialized object which was downloaded from the BucketFS
        """
        with NamedTemporaryFile() as temp_file:
            self.read_file_from_bucketfs_to_fileobj(ctx, exa, bucket_config, temp_file)
            temp_file.flush()
            temp_file.seek(0)
            obj = joblib.load(temp_file)
            return obj
