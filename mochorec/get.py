# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import tempfile
import logging
import re
from mochorec.utils import which, exec_cmd
from mochorec.niconico import Niconico


def main(args):
    url_check = re.match(r'http:\/\/live.nicovideo.jp/watch/(?P<lv>lv[0-9]+)', args.url)
    if url_check is None:
        sys.exit("✗ Incorrect URL patterns")
    lv = url_check.groupdict().get('lv')
    if lv:
        nico = Niconico()
        nico.login()
        status = nico.getplayerstatus(lv)
    else:
        sys.exit("Error")

    saveto = args.savepath if args.savepath else "{}.flv".format(lv)
    if status:
        return get(status, saveto)


def get(param, saveto, cmd="rtmpdump"):
    """get file using rtmpdump"""
    command = which(cmd)
    if not command:
        logging.critical("✗ rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    tempdir = tempfile.mkdtemp()
    contents = param.get('content')
    for i, content in enumerate(contents):
        save_tmp = os.path.join(tempdir, str(i))
        com = "{rtmp} -r {url} -y mp4:/{content} -C S:{ticket} -e -o {saveto}".format(
            rtmp=command, url=param.get('url'), content=content,
            ticket=param.get('ticket'), saveto=save_tmp)
        logging.critical("==> {}".format(com))
        exec_cmd(com)

    if len(contents) <= 1:
        # rename and move
        os.rename(save_tmp, saveto)
    else:
        logging.critical("Join the files since this files are multiple")
        # combine files
        ffmpeg = which("ffmpeg")

        input_txt = os.path.join(tempdir, "input.txt")
        with open(input_txt, "w") as f:
            txt = "\n".join("file {}".format(
                os.path.join(tempdir, str(i))) for i in range(len(contents)))
            f.write(txt)

        # ffmpeg -f concat -safe 0 -i input.txt -c copy <output.flv>
        com = '{ffmpeg} -f concat -safe 0 -i {input_txt} -c copy {saveto}'.format(
            ffmpeg=ffmpeg, input_txt=input_txt, saveto=saveto)
        logging.critical("==> {}".format(com))
        exec_cmd(com)
