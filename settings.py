import os


GOOGLE_API_CLIENT_SECRET_FILE = os.environ['GOOGLE_API_CLIENT_SECRET_FILE']
GOOGLE_API_VERSION = 'v3'
GOOGLE_API_SERVICE = 'drive'
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']
APPLICATION_NAME = 'easy-german'
MAX_RESULTS_PER_PAGE = 2
MAX_DOWNLOADS = 5
LOGGING = {
    'general': 'INFO',
    'dependencies': {
        'googleapiclient': 'ERROR',
    },
}
EPISODES_FILE = 'episodes.json'
