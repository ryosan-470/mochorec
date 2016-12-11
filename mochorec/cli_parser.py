# -*- coding: utf-8 -*-
# main.py
# command line parser
import argparse
import sys
import logging
import mochorec.get
import mochorec.convert
import mochorec.mp3tag


def create_parser():
    parser = argparse.ArgumentParser(
        prog="mochorec",
        description="The command line utility for the nicovideo live"
    )
    subparsers = parser.add_subparsers()
    # get <url> (savepath)
    getcmd = subparsers.add_parser(
        'get', help='Download a movie from the nicovideo live')
    getcmd.set_defaults(func=mochorec.get.main)
    getcmd.add_argument("url", type=str)
    getcmd.add_argument("savepath", nargs='?', type=str, default=None)
    # convert <input> (output) (start_time) (cutting_time)
    convertcmd = subparsers.add_parser(
        'convert', help='Convert the input file to the audio file (mp3)')
    convertcmd.set_defaults(func=mochorec.convert.main)
    convertcmd.add_argument("input_file", type=str)
    convertcmd.add_argument("-o", "--output", nargs='?', type=str, default=None)
    convertcmd.add_argument(
        "-s",
        "--starting-time",
        nargs='?',
        default=0,
        type=int
    )
    convertcmd.add_argument(
        "-c",
        "--cutting-time",
        nargs='?',
        default=1800,
        type=int
    )
    # mp3tag <mp3_file> --artist_name <artist> --title <title> --album_name <album> --cover <cover_file_path> --truck_number <number>
    mp3tagcmd = subparsers.add_parser(
        'mp3tag', help='Add tag for your mp3 file'
    )
    mp3tagcmd.set_defaults(func=mochorec.mp3tag.main)
    mp3tagcmd.add_argument("mp3file", type=str)
    mp3tagcmd.add_argument("--artist_name", nargs='?', type=str, default="")
    mp3tagcmd.add_argument("-t", "--title", nargs='?', type=str, default="")
    mp3tagcmd.add_argument("--album_name", nargs='?', type=str, default="")
    mp3tagcmd.add_argument("--cover", nargs='?', type=str, default="")
    mp3tagcmd.add_argument("--track_number", nargs='?', type=int, default=0)
    # DEBUG
    parser.add_argument(
        "--debug", "-d",
        help="debug: show more messages for your debug",
        action='store_true'
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    if "func" not in dir(args):
        sys.exit(parser.print_help())

    # logger level
    if args.debug is True:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(format='%(message)s', level=level)
    args.func(args)
