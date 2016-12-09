# -*- coding: utf-8 -*-
import logging
import string
import sys
import tempfile
import os
import random
from mochorec.utils import which, exec_cmd


def main(args):
    output = args.output
    if output is None:
        name = os.path.splitext(args.input_file)[0]
        output = "{}.mp3".format(name)
    return convert(
        args.input_file,
        args.starting_time,
        args.cutting_time,
        output
    )


def convert(source_path, start_time, cutted_time, output_path):
    """Cutting and convert video using ffmpeg"""
    ffmpeg = which("ffmpeg")
    if not ffmpeg:
        logging.critical("✗ rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    # 1. cut file
    tempdir = tempfile.mkdtemp()
    random_base = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(20)])
    temp = os.path.join(tempdir, random_base + ".flv")
    # ffmpeg -ss <start_time> -i <source> -t <cutted_time> <output_path>
    com = "{ffmpeg} -ss {start_time} -i {source} -t {cutted_time} {temp_path}".format(
        ffmpeg=ffmpeg, start_time=start_time, source=source_path,
        cutted_time=cutted_time, temp_path=temp)
    logging.critical("==> {}".format(com))
    exec_cmd(com)

    # 2. flv to mp3
    # ffmpeg -i <temp> -acodec libmp3lame -ab 256k <output_path>
    com = "{ffmpeg} -i {temp_path} -acodec libmp3lame -ab 256k {output_path}".format(
        ffmpeg=ffmpeg, temp_path=temp, output_path=output_path)
    logging.critical("==> {}".format(com))
    exec_cmd(com)
    logging.critical("✓ Converted: {}".format(output_path))

