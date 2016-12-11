# -*- coding: utf-8 -*-
import os
from mutagen.id3 import ID3, TPE1, TIT2, TALB, TRCK, APIC
from mutagen.mp3 import MP3


def addtag(mp3file, artist_name, title, album_name, track_number, cover_path):
    m = MP3(mp3file, ID3=ID3)
    m["TPE1"] = TPE1(encoding=3, text=artist_name)
    m["TIT2"] = TIT2(encoding=3, text=title)
    m["TALB"] = TALB(encoding=3, text=album_name)
    m["TRCK"] = TRCK(encoding=3, text="{}".format(track_number))
    if os.path.exists(cover_path):
        with open(cover_path, "rb") as d:
            m.tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc='Cover',
                    data=d.read()
                )
            )

    print(m)
    m.save()
    return True


def main(args):
    addtag(
        mp3file=args.mp3file,
        artist_name=args.artist_name,
        title=args.title,
        album_name=args.album_name,
        track_number=args.track_number,
        cover_path=args.cover
    )
