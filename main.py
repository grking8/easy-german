import logging
import os
import shutil
import subprocess
import tempfile

from apiclient import discovery
import httplib2
import requests

from drive import create_folder
from drive import get_credentials
from drive import upload_media
import settings

logging.basicConfig(level=logging.getLevelName(settings.LOGGING))
logger = logging.getLogger(__name__)

CHANNEL_ID = 'UCbxb2fqe9oNgglAoYqsYOtQ'
MIME_TYPE = 'audio/mp3'
EXTENSION = 'mp3'
API_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
VIDEO_BASE_URL = 'https://www.youtube.com/watch?v={}'


def clear_local_media(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)


def process_items(service, items, videos_downloaded):
    logger.info('Processing up to {} items'.format(len(items)))
    result = 0
    for item in items:
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
            logger.info('Processed successfully video: {}, title: {}'.format(
                video_id, video_title))
            result += 1
        except Exception:
            logger.exception(
                'Error processing video: {}, title: {}'.format(
                    video_id, video_title))
        clear_local_media(tmp_dir)
        if result + videos_downloaded >= settings.MAX_DOWNLOADS:
            logger.info('Stopping as maximum number of videos downloaded')
            logger.info('{} videos processed in this batch'.format(result))
            return result
    logger.info('{} videos processed in this batch'.format(result))
    return result


def main():
    videos_downloaded = 0
    logger.info('Getting credentials and authorising for Google Drive')
    try:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        logger.info('Google Drive authorisation successful')
    except Exception:
        logger.exception(
            'Unable to get credentials and authorise for Google Drive')
    service = discovery.build(
        settings.GOOGLE_API_SERVICE, settings.GOOGLE_API_VERSION, http=http)
    if service:
        logger.info('Getting playlist id')
        try:
            r = requests.get('{}channels?part=contentDetails&id={}&key={}'
                             .format(API_BASE_URL, CHANNEL_ID,
                                     settings.YOUTUBE_KEY))
            playlist_id = (r.json()['items'][0]['contentDetails']
                           ['relatedPlaylists']['uploads'])
            logger.info('Playlist id retrieved successfully')
        except Exception:
            logger.exception('Unable to get playlist id')
        if playlist_id:
            logger.info('Attempting to download a maximum of {} videos'.format(
                settings.MAX_DOWNLOADS))
            s_js = requests.get(
                '{}playlistItems?part=snippet&maxResults={}&playlistId={}'
                '&key={}'
                .format(API_BASE_URL, settings.MAX_RESULTS_PER_PAGE,
                        playlist_id, settings.YOUTUBE_KEY)).json()
            videos_downloaded += process_items(
                service, s_js.get('items', []), videos_downloaded)
            logger.info('{} videos downloaded'.format(videos_downloaded))
            next_page_token = s_js.get('nextPageToken')
            while (next_page_token and
                   videos_downloaded < settings.MAX_DOWNLOADS):
                s_js = requests.get(
                    '{}playlistItems?part=snippet&maxResults={}&playlistId={}'
                    '&key={}&pageToken={}'.format(
                        API_BASE_URL, settings.MAX_RESULTS_PER_PAGE,
                        playlist_id, settings.YOUTUBE_KEY, next_page_token)
                ).json()
                videos_downloaded += process_items(
                    service, s_js.get('items', []), videos_downloaded)
                logger.info('{} videos downloaded'.format(videos_downloaded))
                next_page_token = s_js.get('nextPageToken')
            logger.info('Downloading finished, {} videos downloaded'.format(
                videos_downloaded))


main()
