#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta

old_time = datetime.utcnow() - timedelta(hours=1)

# 2020-10-15T01:24:41Z
old_time_str = old_time.strftime("%Y-%m-%dT%H:%M:%SZ")


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyCcgvlQkOmpKreb7DvAKRiGnTjYQ2xjaHk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=1000,
        publishedAfter=old_time_str
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(search_result)
    print(videos)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='corona')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as  e:
        print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))