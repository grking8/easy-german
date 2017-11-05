
from __future__ import print_function
import os

from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from . import settings


try:
    import argparse
    flags = argparse.ArgumentParser(
        parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir, '{}.json'.format(
        settings.APPLICATION_NAME))

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            settings.GOOGLE_API_CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = settings.APPLICATION_NAME

        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)

    return credentials


def upload_media(service, path, mime_type, parents=None, resumable=True):

    if not os.path.isfile(path):
        raise FileNotFoundError('Media file does not exist.')

    file_metadata = {'name': os.path.basename(path)}

    if parents:
        file_metadata['parents'] = parents

    media = MediaFileUpload(
        path, mimetype=mime_type, resumable=resumable)
    return service.files().create(
        body=file_metadata, media_body=media, fields='id,name').execute()


def create_folder(service, name):

    if not isinstance(name, str):
        raise TypeError('Folder name should be a string.')

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    return service.files().create(
        body=file_metadata, fields='id,name').execute()


def delete_file(service, file_id):

    if not isinstance(file_id, str):
        raise TypeError('File id should be a string.')

    return service.files().delete(fileId=file_id).execute()
