import atexit
import logging
import os
import shutil
import subprocess
import tempfile

from apiclient import discovery

from drive import create_folder
from drive import get_credentials
from drive import upload_media

import httplib2

import requests


logger = logging.getLogger(__name__)

CHANNEL_ID = 'UCbxb2fqe9oNgglAoYqsYOtQ'
MIME_TYPE = 'audio/mp3'
EXTENSION = 'mp3'
MAX_RESULTS = 6


def clear_local_media(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    api_base_url = 'https://www.googleapis.com/youtube/v3/'
    r = requests.get('{}channels?part=contentDetails&id={}&key={}'.format(
        api_base_url, CHANNEL_ID, os.environ['YOUTUBE_KEY']))
    playlist_id = r.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']  # noqa
    s = requests.get(
        '{}playlistItems?part=snippet&maxResults={}&playlistId={}&key={}'
        .format(api_base_url, MAX_RESULTS, playlist_id,
                os.environ['YOUTUBE_KEY']))
    video_base_url = 'https://www.youtube.com/watch?v={}'

    for item in s.json()['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_url = video_base_url.format(video_id)
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

        upload_media(service, local_path, MIME_TYPE,
                     parents=[create_folder(service, video_id).get('id')])
        clear_local_media(tmp_dir)
        atexit.unregister(clear_local_media)


if __name__ == '__main__':
    main()
