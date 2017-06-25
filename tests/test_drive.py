import httplib2
import pytest
from apiclient import discovery

from drive import create_folder
from drive import get_credentials
from drive import upload_media

@pytest.fixture
def service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service
    
    
@pytest.mark.parametrize('name', ['testFolderA'])
def test_create_folder(service, name):
    assert create_folder(service, name).get('name') == name
    
    
@pytest.mark.parametrize('name', [23])
def test_create_folder_raises_exception_non_string_name(service, name):
    with pytest.raises(TypeError):
        create_folder(service, name)
        

ASSETS = 'tests/assets/'        
@pytest.mark.parametrize('path,mime_type', 
                         [('{}wombat.png'.format(ASSETS), 'image/png'),
                          ('{}hello.txt'.format(ASSETS), 'text/plain'),
                          ('{}ZdeUwPFB02Y.mp3'.format(ASSETS), 'audio/mp3'),
                          ('{}pytest.pdf'.format(ASSETS), 'application/pdf'),
                          ('{}yellow.jpg'.format(ASSETS), 'image/jpeg')])
def test_upload_media(service, path, mime_type):
    assert upload_media(service, path, mime_type).get('name') in {
        'wombat.png', 'hello.txt', 'ZdeUwPFB02Y.mp3', 'pytest.pdf',
        'yellow.jpg'}
    
    
@pytest.mark.parametrize('path,mime_type',
                         [('path/to/nonexistent/file', 'image/png')])
def test_upload_media_raises_exception_non_existent_file(service, path,
                                                         mime_type):
    with pytest.raises(FileNotFoundError):
        upload_media(service, path, mime_type)
