import os


GOOGLE_API_CLIENT_SECRET_FILE = os.getenv('GOOGLE_API_CLIENT_SECRET_FILE')
GOOGLE_API_VERSION = 'v3'
GOOGLE_API_SERVICE = 'drive'
YOUTUBE_KEY = os.getenv('YOUTUBE_KEY')
APPLICATION_NAME = 'easy-german'
LOGGING = {
    'general': 'INFO',
    'dependencies': {
        'googleapiclient': 'ERROR',
    },
}
EPISODES_FILE = 'episodes.json'
