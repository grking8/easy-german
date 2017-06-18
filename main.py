import httplib2

from apiclient import discovery

from drive import get_credentials
from drive import upload_media

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    path = '/Users/guyking/Documents/How to learn German faster (with Michael from smarterGerman) _ Easy German 199-_JQjnKreDmQ.mp3'
    mime_type = 'audio/mp3'
    upload_media(service, path, mime_type)

if __name__ == '__main__':
    main()