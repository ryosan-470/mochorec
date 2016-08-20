#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mochorec command line tools
import mochorec.niconico as nico
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
    if not command:
        logging.critical("[+] rtmpdump not found. Please install rtmpdump on your PATH")
        sys.exit(1)

    com = "{rtmp} -r {url} -y mp4:/{content} -C S:{ticket} -e -o {saveto}".format(
        rtmp=command, url=param.get('url'), content=param.get('content'),
        ticket=param.get('ticket'), saveto=saveto
    )
    logging.debug(com)


def main():
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    n = nico.Niconico()
    n.login()
    logging.info("[+] Login success")

    status = n.getplayerstatus("lv272216525")
    logging.info("[+] start download")

    download(status, "./toramamo137.flv")


if __name__ == "__main__":
    main()
