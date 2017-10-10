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
MAX_RESULTS = 1
API_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
VIDEO_BASE_URL = 'https://www.youtube.com/watch?v={}'
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']


def clear_local_media(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    r = requests.get('{}channels?part=contentDetails&id={}&key={}'.format(
        API_BASE_URL, CHANNEL_ID, YOUTUBE_KEY))
    playlist_id = r.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']  # noqa
    s = requests.get(
        '{}playlistItems?part=snippet&maxResults={}&playlistId={}&key={}'
        .format(API_BASE_URL, MAX_RESULTS, playlist_id,
                YOUTUBE_KEY))

    for item in s.json()['items']:
        video_title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        video_url = VIDEO_BASE_URL.format(video_id)
        tmp_dir = tempfile.mkdtemp()

        try:
            subprocess.check_output(['youtube-dl', '--extract-audio',
                                     '--audio-format', EXTENSION, '--output',
                                     os.path.join(tmp_dir, '%(id)s.%(ext)s'),
                                     video_url])
            local_path = os.path.join(
                tmp_dir, '{}.{}'.format(video_id, EXTENSION))
            upload_media(service, local_path, MIME_TYPE,
                         [create_folder(service, video_title).get('id')])
        except Exception:
            logger.exception(
                'Error downloading or processing video {}, title {}.'.format(
                    video_id, video_title))

        clear_local_media(tmp_dir)


if __name__ == '__main__':
    main()
