#!/usr/bin/env python3
import json
import requests


URL = {
    "login": "https://secure.nicovideo.jp/secure/login?site=niconico",
    "search": "http://api.search.nicovideo.jp/api/v2/live/contents/search",
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

    def search(self, query):
        # http://search.nicovideo.jp/docs/api/search.html

        # query='targets=title&fields=contentId,title,viewCounter&_sort=-startTime&_offset=0&_limit=3&_context=test'
        # curl --globoff http://api.search.nicovideo.jp/api/v2/live/contents/search?${query} --data-urlencode "q=TrySailのTRYangle harmony" | jq
        params = {
            'targets': 'title',
            'fields': 'contentId,title,viewCounter,startTime,liveStatus',
            '_sort': '-startTime', # 降順
            '_offset': 0,
            '_limit': 3,
            '_context': 'mochorec : https://github.com/jtwp470/mochorec',
            'q': query
        }

        r = requests.get(URL['search'], params=params)
        print(r.url)
        print(r.text)
        print(r.json())


class LoginError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Login failed: " + self.msg

n = Niconico()
n.search("TrySailのTRYangle harmony")
