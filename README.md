## Description

Download [Easy German](http://easygerman.org/) videos and transcripts.

## Setup

- Create a virtual environment, e.g. `mkvirtualenv easy-german`

- `pip install easygerman`

- Download credentials file for Google APIs into home directory

- Set environment variables (see `settings.py`)

- Run tests: `pytest`

## Usage

```
import easy_german

easy_german.get_videos(max_downloads=150, max_results_per_page=20)
easy_german.get_transcripts()
```
