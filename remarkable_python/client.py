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

    def get_file(self, file_id):
        body = json.dumps({'http_method': 'GET', 'relative_path': file_id})
        response = requests.post(API_DOWNLOAD, data=body, headers=self.headers)

        if response.status_code != 200:
            raise Exception("Error getting file: " + response.content.decode('ascii'))

        file_location = response.json()['url']
        response = requests.get(file_location, headers=self.headers)

        return response.content.decode('ascii')

    def get_root_index(self):
        root_index_id = self.get_file(self.ROOT_FILE_ID)

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

        return response.content