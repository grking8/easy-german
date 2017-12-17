"""Download audio of Easy German videos and upload to Google Drive."""
from . import videos
from . import transcripts


def get_videos(max_downloads=1, max_results_per_page=10):
    """
    Scrape video audio and upload to Google Drive.

    :param int max_downloads: Maximum number of video audios to scrape and
                              download.
    :param int max_results_per_page: Maximum number in each batch; less than or
                                     equal to 50 as per YouTube API pagination.
    """
    videos.main(max_downloads, max_results_per_page)


def get_transcripts():
    """Scrape video transcripts and upload to Google Drive."""
    transcripts.main()
