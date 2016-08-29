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


def download(param, saveto, cmd="rtmpdump"):
    """download file using rtmpdump"""
    command = which(cmd)
    saveto = saveto[0]
    if not command:
        logging.critical("[+] rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    com = "{rtmp} -r {url} -y mp4:/{content} -C S:{ticket} -e -o {saveto}".format(
        rtmp=command, url=param.get('url'), content=param.get('content'),
        ticket=param.get('ticket'), saveto=saveto
    )
    logging.debug(com)
    logging.info("[+] Starting download")
    try:
        subprocess.check_call(shlex.split(com))
        logging.info("[+] Complete download file: " + saveto)
    except:
        logging.warn("Failed to execute command: " + com)


def parse():
    parser = argparse.ArgumentParser(description="mochorec")
    # -lv lv*********
    parser.add_argument("-lv", help="lv is niconico video movie id",
                        required=True, nargs=1)
    # save path
    parser.add_argument("--save", "-s", help="file save path and name",
                        required=True, nargs=1)
    # DEBUG
    parser.add_argument("--debug", "-d", help="debug: show more messages for your debug",
                        action='store_true')
    return parser.parse_args()


def main():
    arg = parse()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)
    if arg.debug is True:
        logging.level = logging.DEBUG
    n = nico.Niconico()
    n.login()
    logging.info("[+] Login success")

    status = n.getplayerstatus(arg.lv)
    download(status, arg.save)


if __name__ == "__main__":
    main()
