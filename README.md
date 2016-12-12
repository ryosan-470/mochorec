# mochorec

[![Build Status](https://travis-ci.com/jtwp470/mochorec.svg?token=6crSMqpz9hor3RSfEisa&)](https://travis-ci.com/jtwp470/mochorec)

もちょ ヾ(@>▽<@)ノ (○・▽・○)  (*゜0゜) かわいいよね

ニコニコ動画のタイムシフト予約自動化 + 動画をダウンロードし適切な形に変換するスクリプトです.

## How to install

```bash
$ git clone https://github.com/jtwp470/mochorec
$ cd mochorec
$ python setup.py install
$ mochorec -h
usage: mochorec [-h] [--debug] {get,convert} ...

The command line utility for the nicovideo live

positional arguments:
  {get,convert,mp3tag}
    get          Download a movie from the nicovideo live
    convert      Convert the input file to the audio file (mp3)
    mp3tag              Add tag for your mp3 file

optional arguments:
  -h, --help     show this help message and exit
  --debug, -d    debug: show more messages for your debug
```

## Usage

### Get file from the nicovideo live
```bash
$ mochorec get <url>
```

### Convert the movie to audio (mp3) file and cut
The following command, cut the movie from the position of 30 mins (1800 secs) 15 minutes (900 secs).

```bash
$ mochorec convert <input_movie_file> -o <output_mp3_file> -s 1800 -c 900
```

### Add to tag your mp3 file

```bash
$ mochorec mp3tag <input_mp3_file> \
    --artist_name "TrySail" \
    --title "High Free Spirits" \
    --album_name "High Free Spirits" \
    --cover "<input_cover_file>" \
    --track_number 1
```

## Configutation
Please set the mail address and password as follows.

### Save to file (Recommended)
Save the configuration file at `~/.mochorec/config.json`:

```json
{
	"nicovideo_mail": <your_mail_address>
	"nicovideo_password": <your_nicovideo_password>
}
```

### Environment Variables

```bash
export NICOVIDEO_MAIL=<your_mail_address>
export NICOVIDEO_PASSWORD=<your_nicovideo_password>
```


## License
This program is licensed under the [GNU General Public License Version 2](./LICENSE.txt).

Author: Ryosuke SATO <rskjtwp@gmail.com>
