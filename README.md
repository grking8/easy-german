## Description

Download [Easy German](http://easygerman.org/) videos and transcripts (subtitles) and upload to Google Drive.

## Setup (Mac OS X / Linux)

- `pip install easygerman` (Python 3+)
- Enable YouTube and Google Drive APIs in Google Developer Console
- Create an API key https://console.developers.google.com/apis/credentials
- Add `export YOUTUBE_KEY=<apikey>` to `~/.bash_profile` or `~/.bashrc`
- Follow a-g in [Step 1](https://developers.google.com/drive/v3/web/quickstart/python) and add another environment variable in `~/.bash_profile` or `~/.bashrc` called `GOOGLE_API_CLIENT_SECRET_FILE` pointing to the path of the downloaded file
- `source ~/.bashrc` or `source ~/.bash_profile`
- In `~/.credentials` there should be a `JSON` file, e.g. `drive-python-quickstart.json`. Rename this to `easy-german.json`

## Usage
```
import easy_german

easy_german.get_videos(max_downloads=150, max_results_per_page=20)
easy_german.get_transcripts()
```

## Documentation

- [Code](https://readthedocs.org/)
- [Wiki](https://family-guy.github.io/easy-german-wiki/)

## License

[MIT](http://opensource.org/licenses/MIT)

## Contributing

See [here.](https://gist.github.com/Chaser324/ce0505fbed06b947d962#accepting-and-merging-a-pull-request)