#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mochorec command line tools
import mochorec.niconico as nico
import sys
import os


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
        sys.stderr.stdout("[+] Error: {} not found.".format(cmd))
        sys.exit(1)

    com = "{rtmp} -r {url} -y mp4:/{content} -C S:{ticket} -e -o {saveto}".format(
        rtmp=command, url=param.get('url'), content=param.get('content'),
        ticket=param.get('ticket'), saveto=saveto
    )
    print(com)


def main():
    n = nico.Niconico()
    n.login()
    print("[+] Login success")

    status = n.getplayerstatus("lv272216525")
    print("[+] start download")

    download(status, "./toramamo137.flv")


if __name__ == "__main__":
    main()
