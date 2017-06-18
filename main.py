import json
import subprocess

import requests
import httplib2
from apiclient import discovery

from drive import get_credentials
from drive import upload_media

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    youtube_key_path = 'key.txt'
    with open(youtube_key_path, 'r') as f:
        youtube_key = f.read()

    part = 'snippet,id'
    order = 'date'
    max_results = 20
    search_url =  'https://www.googleapis.com/youtube/v3/search?key={}&part={}&order={}&maxResults={}'.format(youtube_key, part, order, max_results)

    resp = requests.get(search_url)
    js = json.loads(resp.text)
    items = js['items']
    
    base_url = 'https://www.youtube.com/watch?v={}'
    video_id = items[0]['id']['videoId']
    video_url = base_url.format(video_id)
    
    subprocess.check_output(['youtube-dl', video_url, '--extract-audio',
                            '--audio-format', 'mp3'])
    mime_type = 'audio/mp3'
    filename = '{}-{}.{}'.format(items[0]['snippet']['title'].replace('|', '_'), video_id, mime_type.split('/')[-1])

    upload_media(service, filename, mime_type)
    

if __name__ == '__main__':
    main()

    

