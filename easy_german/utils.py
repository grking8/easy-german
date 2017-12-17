"""Utility functions."""
import logging
import re
import shutil

from apiclient import discovery
import httplib2

from . import drive
from . import settings


for key, val in settings.LOGGING['dependencies'].items():
    logging.getLogger(key).setLevel(logging.getLevelName(val))
logging.basicConfig(level=logging.getLevelName(settings.LOGGING['general']))
logger = logging.getLogger(__name__)


def clear_local_media(tmp_dir):
    """
    Remove directory tree.

    :param str tmp_dir: Path of tree root directory to remove.
    """
    shutil.rmtree(tmp_dir, ignore_errors=True)


def extract_episode(text, seg_search, eg_search):
    """
    Extract episode number from metadata.

    :param str text: Metadata containing episode number.
    :param str seg_search: Regex for a `Super Easy German` episode.
    :param str eg_search: Regex for an `Easy German` episode.
    :return: Episode number and type.
    :rtype: dict
    """
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
    """
    Attempt to authenticate and get Google Drive API service.

    :return: Google Drive API service.
    :rtype: An instance of a Google Drive API class.
    """
    logger.info('Getting credentials and authorising for Google Drive')
    try:
        credentials = drive.get_credentials()
        http = credentials.authorize(httplib2.Http())
        logger.info('Google Drive authorisation successful')
        return discovery.build(
            settings.GOOGLE_API_SERVICE, settings.GOOGLE_API_VERSION,
            http=http)
    except Exception:
        logger.exception(
            'Unable to get credentials and authorise for Google Drive')
