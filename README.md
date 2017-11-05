# Description

Download [Easy German](http://easygerman.org/) videos and transcripts.

## Setup

- Clone the git repository

- Create a virtual environment `mkvirtualenv easy-german`

- `pip install easy-german`

- Download credentials file for Google APIs into home directory

- Update environment variables and set number of videos to download / pagination (see `settings.py`)

- Run tests `pytest`

- Download videos and transcripts `python easy_german/videos.py && python easy_german/transcripts.py`
