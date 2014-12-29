from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
import httplib2


FOLDER_NAME = 'public'
FILE_NAME = 'test_document.txt'
FILE_CONTENT = ''
CLIENT_EMAIL = '911984682386-rr5rg1e4m5v6j0mk89jniqcon26pgjic@developer\
.gserviceaccount.com'
AUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

with open("nudrive.pem") as f:
    PRIVATE_KEY = f.read()


class File(object):

    '''Read all data from file'''

    def __init__(self):
        # self._folder_name = FOLDER_NAME
        self._folder_name = ''
        # self._file_name = FILE_NAME
        self._file_name = ''
        # self._file_content = FILE_CONTENT
        self._file_content = ''
        super(File, self).__init__()

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, value):
        self._folder_name = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_content(self):
        return self._file_content

    @file_content.setter
    def file_content(self, value):
        self._file_content = value


class Authorize(object):

    '''Authrize http object'''

    def __init__(self):
        self._client_email = ''
        self._private_key = ''
        self._auth_scope = ''
        super(Authorize, self).__init__()

    @property
    def client_email(self):
        return self._client_email

    @client_email.setter
    def client_email(self, value):
        self._client_email = value

    @property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value

    @property
    def auth_scope(self):
        return self._auth_scope

    @auth_scope.setter
    def auth_scope(self, value):
        self._auth_scope = value

    @property
    def service(self):
        credentials = SignedJwtAssertionCredentials(
            self._client_email, self._private_key, self._auth_scope)
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('drive', 'v2', http=http)
        return service


class Upload(File, Authorize):

    def __init__(self):
        super(Upload, self).__init__()

    def create_public_folder(self):
        body = {
            'title': self.folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file_ = self.service.files().insert(body=body).execute()

        permission = {
            'value': '',
            'type': 'anyone',
            'role': 'reader'
        }

        self.service.permissions().insert(
            fileId=file_['id'], body=permission).execute()

        return file_

    def set_public_folder(self):
        pass

    def insert_file(self):
        folder_id = self.create_public_folder()['id']
        media_body = MediaFileUpload(
            self.file_name,
            mimetype='text/plain',
            resumable=True)
        body = {
            'title': self.file_name,
            'description': 'A test document',
            'mimeType': 'text/plain',
            'parents': [
                {
                    "kind": "drive#fileLink",
                    "id": folder_id,
                },
            ]
        }

        file_ = self.service.files().insert(
            body=body, media_body=media_body)
        file_ = file_.execute()
        print(
            'www.googledrive.com/host/' +
            folder_id +
            '/' +
            body['title']
        )

if __name__ == '__main__':
    f = Upload()
    f.folder_name = FOLDER_NAME
    f.file_name = FILE_NAME
    f.file_content = FILE_CONTENT
    f.client_email = CLIENT_EMAIL
    f.private_key = PRIVATE_KEY
    f.auth_scope = AUTH_SCOPE
    f.create_public_folder()
    f.insert_file()

