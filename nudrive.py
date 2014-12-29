from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
import httplib2


FOLDER_NAME = 'public'
FILE_NAME = 'document.txt'
FILE_CONTENT = ''
CLIENT_EMAIL = '911984682386-rr5rg1e4m5v6j0mk89jniqcon26pgjic@developer\
.gserviceaccount.com'
AUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

with open("nudrive.pem") as f:
    PRIVATE_KEY = f.read()


class File(object):

    '''Read all data from file'''

    def __init__(self):
        self._folder_name = FOLDER_NAME
        self._file_name = FILE_NAME
        self._file_content = FILE_CONTENT
        super(File, self).__init__()

    @property
    def folder_name(self):
        return self._folder_name

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_content(self):
        return self._file_content


class Authorize(object):

    '''Authrize http object'''

    def __init__(self):
        self._client_email = CLIENT_EMAIL
        self._private_key = PRIVATE_KEY
        self._auth_scope = AUTH_SCOPE
        super(Authorize, self).__init__()

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
    # TODO: implement setter methods
    # f.set_public_folder
    # f.set_file_name
    f.create_public_folder()
    f.insert_file()
