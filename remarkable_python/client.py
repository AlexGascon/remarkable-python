from .auth_credentials import AuthCredentials
from .const import API_DOWNLOAD, USER_TOKEN_URL
from .models.index import Index
from .utils import Utils

import json
from dataclasses import dataclass

import requests

@dataclass
class Client:
    ROOT_FILE_ID = 'root'
    REMARKABLE_CLOUD_CONTENT_ENCODING = 'utf-8'

    def __init__(self):
        self.auth_credentials = AuthCredentials.create_from_file()
        self.headers = {'Authorization': 'Bearer ' + self.auth_credentials.user_token}
    
    def renew_token(self):
        """Fetches a new user_token.

        This is the second step of the authentication of the Remarkable Cloud.
        Before each new session, you should fetch a new user token.
        User tokens have an unknown expiration date.

        Returns:
            True

        Raises:
            AuthError: An error occurred while renewing the user token.
        """

        if not self.auth_credentials.device_token:
            raise Exception("Please register a device first")
        token = self.auth_credentials.device_token
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(USER_TOKEN_URL, data=None, headers=headers)

        if response.ok:
            self.auth_credentials.user_token = response.text
            self.headers = {'Authorization': 'Bearer ' + self.auth_credentials.user_token}
            self.auth_credentials.save_to_file()
            return True
        else:
            raise Exception("Can't renew token: {e}".format(
                e=response.status_code))

    def _get_request(self, content_id):
        body = json.dumps({'http_method': 'GET', 'relative_path': content_id})
        location_response = requests.post(API_DOWNLOAD, data=body, headers=self.headers)

        if location_response.status_code != 200:
            raise Exception("Error getting file: " + self._decode_content(location_response.content))

        file_location = location_response.json()['url']
        return requests.get(file_location, headers=self.headers)

    def get_file(self, file_id):
        response = self._get_request(file_id)
        return self._decode_content(response.content)

    def get_file_bin(self, file_id):
        response = self._get_request(file_id)
        return response.content

    def get_root_index(self):
        response = self._get_request(self.ROOT_FILE_ID)
        root_index_id = self._decode_content(response.content)

        return self.list_files_in_index(root_index_id)

    def list_files_in_index(self, index_id):
        index_content = self.get_file(index_id)
        return Index.parse_from_content(index_content)

    def get_file_bin(self, file_id):
        body = json.dumps({'http_method': 'GET', 'relative_path': file_id})
        response = requests.post(API_DOWNLOAD, data=body, headers=self.headers)

        if response.status_code != 200:
            raise Exception("Error getting file: " + response.content.decode('ascii'))

        file_location = response.json()['url']
        response = requests.get(file_location, headers=self.headers)

    def _decode_content(self, content):
        return content.decode(self.REMARKABLE_CLOUD_CONTENT_ENCODING)