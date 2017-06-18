
from __future__ import print_function
import httplib2
import os

from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
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
    credential_path = os.path.join(credential_dir,
                                   'easy-german.json')

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

def upload_media(service, path, mime_type, resumable=True):
    file_metadata = {'name': path}
    media = MediaFileUpload(path, mimetype=mime_type, resumable=resumable)
    service.files().create(body=file_metadata, media_body=media).execute()
    

# def main():
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('drive', 'v3', http=http)
#
#     path = '/Users/guyking/Documents/How to learn German faster (with Michael from smarterGerman) _ Easy German 199-_JQjnKreDmQ.mp3'
#     mime_type = 'audio/mp3'
#     upload_media(service, path, mime_type)
#
#
#     # file_metadata = { 'name': path}
#     #
#     # media = MediaFileUpload(path, mimetype='audio/mp3', resumable=True)
#     #
#     # service.files().create(body=file_metadata, media_body=media).execute()
#
#
#
#     # results = service.files().list(
# #         pageSize=10,fields="nextPageToken, files(id, name)").execute()
# #     items = results.get('files', [])
# #     if not items:
# #         print('No files found.')
# #     else:
# #         print('Files:')
# #         for item in items:
# #             print('{0} ({1})'.format(item['name'], item['id']))
#
# if __name__ == '__main__':
#     main()