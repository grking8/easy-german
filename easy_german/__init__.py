from . import videos
from . import transcripts


def get_videos(max_downloads=1, max_results_per_page=10):
    #  max_results_per_page <= 50
    videos.main(max_downloads, max_results_per_page)


def get_transcripts():
    transcripts.main()
