
from __future__ import print_function
import os

from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(
        parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'easy-german'


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
        
    credential_path = os.path.join(credential_dir, 'easy-german.json')

    store = Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
            
        print('Storing credentials to ' + credential_path)
        
    return credentials


def upload_media(service, path, mime_type, parents=None, resumable=True):
    
    if not os.path.isfile(path):
        raise FileNotFoundError('Media file does not exist.')
    
    splits = path.rsplit('/', 1)
    
    if len(splits) == 1:
        name = splits[0]
    else:
        name = splits[1]

    file_metadata = {'name': name}
    
    if parents:
        file_metadata['parents'] = parents
    
    media = MediaFileUpload(
        path, mimetype=mime_type, resumable=resumable)
    resp = service.files().create(
        body=file_metadata, media_body=media, fields='id,name').execute()
    return resp


def create_folder(service, name):
    
    if not isinstance(name, str):
        raise TypeError('Folder name should be a string.')
        
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    resp = service.files().create(
        body=file_metadata, fields='id,name').execute()
    return resp
