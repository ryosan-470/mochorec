# -*- coding: utf-8 -*-
import os
import shlex
import subprocess
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


def exec_cmd(command, debug=False):
    try:
        if debug:
            subprocess.check_call(shlex.split(command))
        else:
            subprocess.run(shlex.split(command))
    except subprocess.CalledProcessError as e:
        logging.critical(
            "Error: try to run {cmd}\nsubprocess output: {output}".format(
                cmd=e.cmd, output=e.output))

