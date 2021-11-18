
# TODO

class LoadFsFileFromUDF:
    CONNECTION_NAME = "tensorflow_config"

    def run(self, ctx, exa, bucket_config):
        file_path = ctx.path
        #bucket_config = ctx.bucket_config #mynote this is a string
        bucket_path = "/buckets" + "/" + bucket_config.bucketfs_config.bucketfs_name + "/" + bucket_config.bucket_name + "/"

        text_as_string = open(bucket_path + file_path).read()
        return text_as_string


