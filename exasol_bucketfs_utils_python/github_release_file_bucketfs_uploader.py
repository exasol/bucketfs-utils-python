import requests
from requests.auth import HTTPBasicAuth

from exasol_bucketfs_utils_python.release_link_extractor import ReleaseLinkExtractor


class GithubReleaseFileBucketFSUploader:
    def __init__(self, file_to_download_name, github_user, repository_name, release_name, path_inside_bucket):
        self.file_to_download_name = file_to_download_name
        self.github_user = github_user
        self.repository_name = repository_name
        self.release_name = release_name
        self.path_inside_bucket = path_inside_bucket

    def upload(self, address, username, password):
        """
        This method uploads the GitHub release into a selected Exasol bucket.

        :param address: address in the format :samp:`http://{host}:{port}/{bucket name}`
        :param username: bucket writing username
        :param password: bucket writing password
        :return: none
        """
        download_url = self.__extract_download_url()
        r_download = requests.get(download_url, stream=True)
        upload_url = self.__build_upload_url(address)
        requests.put(upload_url, data=r_download.iter_content(10 * 1024), auth=HTTPBasicAuth(username, password))

    def __build_upload_url(self, address):
        if self.path_inside_bucket:
            address += self.path_inside_bucket
        address += self.file_to_download_name
        return address

    def __extract_download_url(self):
        github_api_link = self.__build_github_api_link()
        release_link_extractor = ReleaseLinkExtractor(github_api_link)
        download_url = release_link_extractor.get_link_by_release_name(self.file_to_download_name)
        return download_url

    def __build_github_api_link(self):
        return "https://api.github.com/repos/{github_user}/{repository_name}/releases/{release_name}".format(
            github_user=self.github_user, repository_name=self.repository_name, release_name=self.release_name)
