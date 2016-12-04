import unittest
import re
from mochorec.niconico import Niconico


class NiconicoTest(unittest.TestCase):
    def setUp(self):
        self.nico = Niconico()

    def test_login_success(self):
        n = self.nico
        n.login()
        self.assertEqual(True, n.logined)
        self.assertIn("user_session_", n.session)

    def test_login_failure(self):
        pass

    def test_search(self):
        n = self.nico.search("TrySail")
        cnt = 0

        for d in n.get('data'):
            if d.get('title'):
                cnt += 1
        self.assertEqual(3, cnt)

    def test_getplayerstatus(self):
        n = self.nico
        n.login()
        lvs = ["lv283755462", "lv283755466"]
        for lv in lvs:
            status = n.getplayerstatus(lv)
            # {'ticket': '63159380:lv283755462:0:1480841526:855ad3d58c6f51e8', 'url': 'rtmp://nleu12.live.nicovideo.jp:1935/liveedge/live_161204_17_9'}
            self.assertIn('ticket', status)
            self.assertIn('url', status)
            self.assertRegex(status['url'], '^rtmp://\w+\.live\.nicovideo\.jp:\d+')
            self.assertIn(lv, status['ticket'])
