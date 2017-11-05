import logging
import re
import shutil

from apiclient import discovery
import httplib2

from easy_german.drive import get_credentials
from . import settings


for key, val in settings.LOGGING['dependencies'].items():
    logging.getLogger(key).setLevel(logging.getLevelName(val))
logging.basicConfig(level=logging.getLevelName(settings.LOGGING['general']))
logger = logging.getLogger(__name__)


def clear_local_media(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)


def extract_episode(text, seg_search, eg_search):
    seg_match = re.search(seg_search, text, re.IGNORECASE)
    if seg_match:
        return {
            'type': 'super_easy_german',
            'number': seg_match.group().strip().replace('(', '').replace(
                ')', '')
        }
    eg_match = re.search(eg_search, text, re.IGNORECASE)
    if eg_match:
        return {
            'type': 'easy_german',
            'number': eg_match.group().strip()
        }


def get_gdrive_service():
    logger.info('Getting credentials and authorising for Google Drive')
    try:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        logger.info('Google Drive authorisation successful')
        return discovery.build(
            settings.GOOGLE_API_SERVICE, settings.GOOGLE_API_VERSION,
            http=http)
    except Exception:
        logger.exception(
            'Unable to get credentials and authorise for Google Drive')
