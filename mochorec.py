#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mochorec command line tools
import mochorec.niconico as nico
import argparse
import shlex
import subprocess
import sys
import os
import logging
import re
import tempfile


def which(command):
    """looks like which command on the shell"""
    for path in os.environ.get('PATH').split(os.pathsep):
        command_path = os.path.join(path, command)
        if os.path.exists(command_path):
            return command_path
    # not on PATH?
    if os.path.exists(command):
        return command
    return False


def get(param, saveto, cmd="rtmpdump"):
    """get file using rtmpdump"""
    command = which(cmd)
    if not command:
        logging.critical("[+] rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    tempdir = tempfile.mkdtemp()
    contents = param.get('content')
    for i, content in enumerate(contents):
        save_tmp = os.path.join(tempdir, str(i))
        com = "{rtmp} -r {url} -y mp4:/{content} -C S:{ticket} -e -o {saveto}".format(
            rtmp=command, url=param.get('url'), content=content,
            ticket=param.get('ticket'), saveto=save_tmp)
        logging.debug(com)
        logging.info("[+] Starting get")
        try:
            subprocess.check_call(shlex.split(com))
            logging.info("[+] Complete get file: " + saveto)
        except:
            logging.warn("Failed to execute command: " + com)

    if len(contents) <= 1:
        # rename and move
        os.rename(os.path.join(tempdir, str(i), saveto))
    else:
        # combine files
        ffmpeg = which("ffmpeg")

        input_txt = os.path.join(tempdir, "input.txt")
        with open(input_txt, "w") as f:
            txt = "\n".join("file {}".format(os.path.join(tempdir, str(i))) for i in range(len(contents)))
            f.write(txt)

        # ffmpeg -f concat -safe 0 -i input.txt -c copy <output.flv>
        com = '{ffmpeg} -f concat -safe 0 -i {input_txt} -c copy {saveto}'.format(
            ffmpeg=ffmpeg, input_txt=input_txt, saveto=saveto)
        logging.debug(com)
        try:
            subprocess.check_call(shlex.split(com))
            logging.info("[+] Complete get file: " + saveto)
        except:
            logging.warn("Failed to execute command " + com)


def convert(source_path, start_time, cutted_time, output_path):
    ffmpeg = which("ffmpeg")
    if not ffmpeg:
        logging.critical("[+] rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    # 1. cut file
    temp = tempfile.mkstemp(suffix=".flv")
    # ffmpeg -ss <start_time> -i <source> -t <cutted_time> <output_path>
    com = "{ffmpeg} -ss {start_time} -i {source} -t {cutted_time} {temp_path}".format(
        ffmpeg=ffmpeg, start_time=start_time, source=source_path,
        cutted_time=cutted_time, temp_path=temp[1])
    logging.debug(com)
    try:
        subprocess.check_call(shlex.split(com))
        logging.info("[+] Cutted")
    except:
        logging.warn("Failed to execute command " + com)

    # 2. flv to mp3
    # ffmpeg -i <temp> -acodec libmp3lame -ab 256k <output_path>
    com = "{ffmpeg} -i {temp_path} -acodec libmp3lame -ab 256k {output_path}".format(
        ffmpeg=ffmpeg, temp_path=temp[1], output_path=output_path)
    logging.debug(com)
    try:
        subprocess.check_call(shlex.split(com))
        logging.info("[+] Converted: " + output_path)
    except:
        logging.warn("Failed to execute command " + com)


def login():
    n = nico.Niconico()
    n.login()
    logging.info("[+] Login success")
    return n


def parse():
    parser = argparse.ArgumentParser(prog="mochorec", description="mochorec")
    subparsers = parser.add_subparsers()
    get = subparsers.add_parser('get',
                                help='get http://live.nicovideo.jp/watch/lv********')
    get.add_argument("url", type=str)
    get.add_argument("-s", "--save", help="save path and file name", type=str)

    convert = subparsers.add_parser('convert', help='convert -i <input> -s <start time>(s) -t <cut time>(s) -o <save path>')
    convert.add_argument("-i", "--input", help="input filepath and filename",
                         required=True, type=str)
    convert.add_argument("-s", "--start", help="start time",
                         default=1800)
    convert.add_argument("-t", help="cutting time", nargs=1, default=1770)
    convert.add_argument("-o", "--output", help="output filepath and filename",
                         type=str)
    # DEBUG
    parser.add_argument("--debug", "-d", help="debug: show more messages for your debug",
                        action='store_true')
    # Quiet
    parser.add_argument("--quiet", "-q", help="quiet: not output for stdout",
                        action='store_true')
    return parser.parse_args()


def main():
    arg = vars(parse())
    if arg.get('debug') is True:
        level = logging.NOTSET
    elif arg.get('quiet') is True:
        level = logging.CRITICAL
    else:
        level = logging.INFO
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=level)
    # get
    if arg.get('url'):
        url_check = re.match(r'http:\/\/live.nicovideo.jp/watch/(?P<lv>lv[0-9]+)', arg.get('url'))
        if url_check is None:
            sys.exit("Incorrect url patterns")
        lv = url_check.groupdict().get('lv')
        if lv:
            n = login()
            status = n.getplayerstatus(lv)
        else:
            sys.exit("Incorrect url patterns")
        name = arg.get('save') if arg.get('save') else lv + ".flv"
        if status:
            get(status, name)
        else:
            sys.exit("Error")
    # convert
    elif arg.get('input') and arg.get('start') and arg.get('t') and arg.get('output'):
        i = arg.get('input')[0]
        s = arg.get('start')[0]
        t = arg.get('t')[0]
        o = arg.get('output')[0]
        convert(i, s, t, o)


if __name__ == "__main__":
    main()
