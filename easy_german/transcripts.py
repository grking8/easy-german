import io
import json
import logging
import mimetypes
import os
import tempfile
import zipfile

import requests

from easy_german.drive import upload_media
import easy_german.settings as settings
import easy_german.utils as utils


for key, val in settings.LOGGING['dependencies'].items():
    logging.getLogger(key).setLevel(logging.getLevelName(val))
logging.basicConfig(level=logging.getLevelName(settings.LOGGING['general']))
logger = logging.getLogger(__name__)

URL = 'https://www.dropbox.com/sh/o8ea17w720i4zgs/AACXZG3l3IkAjcO-0tz7EJlLa?dl=1'  # noqa
SEG_SEARCH = r'(?<=SEG) \d{0,5}'
EG_SEARCH = r'(?<=EG) \d{0,5}'


def main():
    gdrive_service = utils.get_gdrive_service()
    if gdrive_service:
        tmp_dir = tempfile.mkdtemp()
        logger.info('Downloading transcripts')
        try:
            r = requests.get(URL)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(tmp_dir)
            logger.info('Transcripts successfully downloaded')
        except Exception:
            logger.exception('Unable to download transcripts')
        if z:
            with open(settings.EPISODES_FILE) as f:
                video_episodes = json.load(f)
            for filename in os.listdir(tmp_dir):
                filepath = os.path.join(tmp_dir, filename)
                if os.path.isfile(filepath):
                    episode = utils.extract_episode(filename, SEG_SEARCH,
                                                    EG_SEARCH)
                    if episode:
                        folder_id = video_episodes[episode['type']].get(
                            episode['number'])
                        if folder_id:
                            logger.info(
                                'Uploading transcript {} for episode type: {},'
                                ' episode number: {}'.format(
                                    filename, episode['type'],
                                    episode['number']))
                            upload_media(
                                gdrive_service,
                                filepath,
                                mimetypes.guess_type(filename),
                                [folder_id])
            utils.clear_local_media(tmp_dir)
            os.remove(settings.EPISODES_FILE)
