import json
import logging
import os
import subprocess
import tempfile

import requests

from easy_german.drive import create_folder
from easy_german.drive import upload_media
import easy_german.settings as settings
import easy_german.utils as utils


for key, val in settings.LOGGING['dependencies'].items():
    logging.getLogger(key).setLevel(logging.getLevelName(val))
logging.basicConfig(level=logging.getLevelName(settings.LOGGING['general']))
logger = logging.getLogger(__name__)

CHANNEL_ID = 'UCbxb2fqe9oNgglAoYqsYOtQ'
MIME_TYPE = 'audio/mp3'
EXTENSION = 'mp3'
API_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
VIDEO_BASE_URL = 'https://www.youtube.com/watch?v={}'
EPISODES = {
    'easy_german': {},
    'super_easy_german': {},
}
SEG_SEARCH = r'(?<=Super Easy German) \(\d{0,5}\)'
EG_SEARCH = r'(?<=Easy German) \d{0,5}'


def process_items(gdrive_service, items, videos_downloaded, max_downloads):
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
            folder_id = create_folder(gdrive_service, video_title).get('id')
            upload_media(gdrive_service, local_path, MIME_TYPE, [folder_id])
            episode = utils.extract_episode(video_title, SEG_SEARCH, EG_SEARCH)
            if episode:
                EPISODES[episode['type']][episode['number']] = folder_id
            logger.info('Processed successfully video: {}, title: {}'.format(
                video_id, video_title))
            result += 1
        except Exception:
            logger.exception(
                'Error processing video: {}, title: {}'.format(
                    video_id, video_title))
        utils.clear_local_media(tmp_dir)
        if result + videos_downloaded >= max_downloads:
            logger.info('Stopping as maximum number of videos downloaded')
            logger.info('{} videos processed in this batch'.format(result))
            return result
    logger.info('{} videos processed in this batch'.format(result))
    return result


def main(max_downloads, max_results_per_page):
    videos_downloaded = 0
    gdrive_service = utils.get_gdrive_service()
    if gdrive_service:
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
            logger.info('Attempting to download up to {} videos'.format(
                max_downloads))
            s_js = requests.get(
                '{}playlistItems?part=snippet&maxResults={}&playlistId={}'
                '&key={}'
                .format(API_BASE_URL, max_results_per_page, playlist_id,
                        settings.YOUTUBE_KEY)).json()
            videos_downloaded += process_items(
                gdrive_service, s_js.get('items', []), videos_downloaded,
                max_downloads)
            logger.info('{} videos downloaded'.format(videos_downloaded))
            next_page_token = s_js.get('nextPageToken')
            while (next_page_token and
                   videos_downloaded < max_downloads):
                s_js = requests.get(
                    '{}playlistItems?part=snippet&maxResults={}&playlistId={}'
                    '&key={}&pageToken={}'.format(
                        API_BASE_URL, max_results_per_page, playlist_id,
                        settings.YOUTUBE_KEY, next_page_token)
                ).json()
                videos_downloaded += process_items(
                    gdrive_service, s_js.get('items', []), videos_downloaded,
                    max_downloads)
                logger.info('{} videos downloaded'.format(videos_downloaded))
                next_page_token = s_js.get('nextPageToken')
            logger.info('Downloading finished, {} videos downloaded'.format(
                videos_downloaded))
            with open(settings.EPISODES_FILE, 'w') as f:
                json.dump(EPISODES, f)
