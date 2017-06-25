import httplib2
import pytest
from apiclient import discovery

from drive import create_folder
from drive import get_credentials

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
