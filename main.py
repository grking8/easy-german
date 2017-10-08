import os
import subprocess

from apiclient import discovery

from drive import get_credentials
from drive import upload_media

import httplib2

import requests


CHANNEL_ID = 'UCbxb2fqe9oNgglAoYqsYOtQ'
MIME_TYPE = 'audio/mp3'
EXTENSION = 'mp3'
MAX_RESULTS = 2
ORDER = 'date'
PART = 'snippet,id'


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    qs = 'key={}&channelId={}&part={}&order={}&maxResults={}'.format(
        os.environ['YOUTUBE_KEY'], CHANNEL_ID, PART, ORDER, MAX_RESULTS)
    search_url = '{}?{}'.format(search_url, qs)
    items = requests.get(search_url).json()['items']
    video_url = 'https://www.youtube.com/watch?v={}'

    for item in items:
        video_id = item['id']['videoId']
        subprocess.check_output(['youtube-dl', '--extract-audio',
                                 '--audio-format', 'mp3', '--id', '--newline',
                                 '--verbose', video_url.format(video_id)])
        path = '{}.{}'.format(video_id, EXTENSION)
        upload_media(service, path, MIME_TYPE)


if __name__ == '__main__':
    main()
