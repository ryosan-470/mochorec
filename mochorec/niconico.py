import json
import sys
import re
import requests
import pprint
from xml.etree.ElementTree import *


URL = {
    "login": "https://secure.nicovideo.jp/secure/login?site=niconico",
    "search": "http://api.search.nicovideo.jp/api/v2/live/contents/search",
    "status": "http://watch.live.nicovideo.jp/api/getplayerstatus",
    "check": "http://live.nicovideo.jp/api/getplayerstatus/nsen/vocaloid",
    "reservation": "http://live.nicovideo.jp/api/watchingreservation",
    "logout": "https://secure.nicovideo.jp/secure/logout",
}


class Niconico:
    def __init__(self):
        self.logined = False
        self.session = ""

    def login(self):
        with open('config.json') as f:
            conf = json.load(f)

        auth = {
            'mail': conf['nicovideo-mail'],
            'password': conf['nicovideo-pass']
            }
        r = requests.post(URL["login"], data=auth, allow_redirects=False)
        session = r.cookies.get('user_session')
        # 再度取得したクッキーを用いてログインリクエストを送る
        r = requests.get(URL["login"], cookies={'user_session': session})
        if r.headers['x-niconico-authflag'] != "1":
            raise LoginError("")

        self.logined = True
        self.session = session

    def logout(self):
        print(self.session)
        r = requests.post(URL["logout"], cookies={'user_session': self.session})
        del self.session
        self.logined = False

    def isLoggedIn(self):
        if self.session == "":
            return False
        r = requests.get(URL["check"], cookies={'user_session': self.session})
        auth = r.headers.get('x-niconico-authflag')
        if not auth or auth != "1":
            return False
        return True

    def search(self, query):
        # not requirements login
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
        return r.json()

    def getplayerstatus(self, lv):
        r = requests.get(URL['status'], params={'v': lv},
                         cookies={'user_session': self.session})
        # tree = parse(r.text)
        root = fromstring(r.text)
        param = {}
        if root.attrib.get('status', 'fail') == 'fail':
            return param

        for child in root:
            if child.tag == "stream":
                for c in child:
                    if c.tag == "quesheet":
                        for q in (c.findall('que')):
                            if "publish" in q.text:
                                content = q.text[q.text.find('/content'):]
                                p = param.get('content')
                                if p:
                                    param.get('content').append(content)
                                else:
                                    param.update({'content': [content]})

            if child.tag == "rtmp":
                param.update({'url': child.find('url').text})
                param.update({'ticket': child.find('ticket').text})
        return param

    def printplayerstatus(self, lv):
        status = self.getplayerstatus(lv)
        pprint.pprint(status)

    def getReservationList(self):
        r = requests.get(URL['reservation'], params={'mode': 'list'},
                        cookies={'user_session': self.session})
        root = fromstring(r.text)
        reservation_id_list = []
        if root.attrib.get('status') == 'fail':
            return reservation_id_list
        timeshift_reserved_list = [vid.text for vid in root[0]]
        return timeshift_reserved_list

    def getToken(self, vid):
        r = requests.get(URL['reservation'], 
                        params={'mode': 'watch_num', 'vid': vid},
                        cookies={'user_session': self.session})
        if "既に予約済みです" in r.text or "申込み期限切れです" in r.text: 
            return False
        else:
            token = re.findall(r'ulck_[0-9]+', r.text)
            if token:
                return token[0]
            raise Exception
    
    def reserve(self, vid):
        token = getToken(vid)
        if not token:
            return False
        r = requests.post(URL['reservation'], 
                        params={'mode': 'regist', 'vid': vid, 'token': token},
                        cookies={'user_session': self.session})
        if r.status_code == 200:
            return True
        else:
            return False
        
    def removeReservation(self, vid):
        # get token
        r = requests.get('http://live.nicovideo.jp/my_timeshift_list',
                cookies={'user_session': self.session})
        token = re.findall(r'ulck_[0-9]+', r.text[r.text.find(str(vid)) + len(str(vid)):])
        if token:
            token = token[0]
        else:
            return False

        print(token)
        r = requests.get('http://live.nicovideo.jp/my',
                params={'delete': 'timeshift', 'vid': vid, 'confirm': token},
                cookies={'user_session': self.session})
        return True


class LoginError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Login failed: " + self.msg


if __name__ == "__main__":
    n = Niconico()
    n.login()
    url_check = re.match(r'http:\/\/live.nicovideo.jp/watch/(?P<lv>lv[0-9]+)', sys.argv[1])
    if url_check is None:
        sys.exit("✗ Incorrect url patterns")
    lv = url_check.groupdict().get('lv')
    if lv:
        n.printplayerstatus(lv)
