# -*- coding: utf-8 -*-
import unittest
from tempfile import mkdtemp
import os
from mochorec.cli_parser import create_parser
import requests
from mutagen.id3 import ID3
from mutagen.mp3 import MP3


def wget(url, savepath):
    r = requests.get(url, stream=True)
    with open(savepath, "wb") as f:
        for chunk in r.iter_content():
            f.write(chunk)


class Mp3Tag(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = mkdtemp()
        print(self.tmp_dir)
        self.mp3file = os.path.join(self.tmp_dir, "test.mp3")
        self.cover = os.path.join(self.tmp_dir, "test.jpg")
        self.parser = create_parser()

        wget("https://archive.org/download/testmp3testfile/mpthreetest.mp3",
             self.mp3file)
        print("Download: {}".format(self.mp3file))
        wget("https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg",
             self.cover)
        print("Download: {}".format(self.cover))

    def testCLIMp3Tag(self):
        artist_name = "TrySail"
        title = "TrySailのトライアングルハーモニー"
        album_name = "Sail Canvas"
        track_number = '160'

        args = self.parser.parse_args(
            [
                'mp3tag', self.mp3file,
                '--artist_name', artist_name,
                '-t', title,
                '--album_name', album_name,
                '--track_number', track_number,
                '--cover', self.cover,
            ]
        )
        args.func(args)
        m = MP3(self.mp3file, ID3=ID3)
        self.assertEqual(m.get('TPE1').text[0], artist_name)
        self.assertEqual(m.get('TIT2').text[0], title)
        self.assertEqual(m.get('TALB').text[0], album_name)
        self.assertEqual(m.get('TRCK').text[0], track_number)
