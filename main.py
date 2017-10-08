import atexit
import logging
import os
import shutil
import subprocess
import tempfile

from apiclient import discovery

from drive import get_credentials
from drive import upload_media

import httplib2

import requests


logger = logging.getLogger(__name__)

CHANNEL_ID = 'UCbxb2fqe9oNgglAoYqsYOtQ'
MIME_TYPE = 'audio/mp3'
EXTENSION = 'mp3'
MAX_RESULTS = 2
ORDER = 'date'
PART = 'snippet,id'


def clear_local_media(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)


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
        video_url = video_url.format(video_id)
        file_name = '{}.{}'.format(video_id, EXTENSION)
        tmp_dir = tempfile.mkdtemp()
        atexit.register(clear_local_media, tmp_dir=tmp_dir)
        local_path = os.path.join(tmp_dir, file_name)

        try:
            subprocess.check_output(['youtube-dl', '--extract-audio',
                                     '--audio-format', 'mp3', '--newline',
                                     '--verbose', '--output', local_path,
                                     video_url])
        except Exception:
            logger.exception('Error downloading video.')

        upload_media(service, local_path, MIME_TYPE)
        clear_local_media(tmp_dir)
        atexit.unregister(clear_local_media)


if __name__ == '__main__':
    main()
