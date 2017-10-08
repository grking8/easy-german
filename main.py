import json
import os
import subprocess

from apiclient import discovery

from drive import get_credentials
from drive import upload_media

import httplib2

import requests


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    channel_id = 'UCbxb2fqe9oNgglAoYqsYOtQ'
    part = 'snippet,id'
    order = 'date'
    max_results = 20
    search_url = 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part={}&order={}&maxResults={}'.format(  # NOQA
        os.environ['YOUTUBE_KEY'], channel_id, part, order, max_results)

    resp = requests.get(search_url)
    js = json.loads(resp.text)
    items = js['items']

    base_url = 'https://www.youtube.com/watch?v={}'
    video_id = items[0]['id']['videoId']
    video_url = base_url.format(video_id)

    subprocess.check_output(['youtube-dl', video_url, '--extract-audio',
                            '--audio-format', 'mp3', '--id', '--verbose'])
    mime_type = 'audio/mp3'
    path = '{}.{}'.format(video_id, mime_type.split('/')[-1])

    upload_media(service, path, mime_type)


if __name__ == '__main__':
    main()
