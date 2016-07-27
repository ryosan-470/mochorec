#!/usr/bin/env python3
import json
import requests


URL = {
    "login": "https://secure.nicovideo.jp/secure/login?site=niconico"
}


class Niconico:
    def __init__(self):
        self.logined = False
        self.headers = None

    def login(self):
        with open('config.json') as f:
            conf = json.load(f)

        auth = {
            'mail': conf['nicovideo-mail'],
            'password': conf['nicovideo-pass']
            }
        r = requests.post(URL["login"], data=auth)

        if r.headers['x-niconico-authflag'] != 1:
            raise LoginError("")
        self.logined = True
        self.headers = r.headers

    def logout(self):
        del(self.logined)
        del(self.headers)


class LoginError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Login failed: " + self.msg
