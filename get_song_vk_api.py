#! -*- coding: utf-8 -*-
from Queue import Queue
import json
import os
import random
from threading import Thread, Lock
import traceback
import urllib
import urllib2
import re
import string
from collections import Iterable
import time
from xml_parse import parse
from selen_page import process
__author__ = 'wilfman'

lock = Lock()


class TaskToThreadPool(object):
    def __init__(self, pool_size, job=None):
        self.pool_size = pool_size
        self.q = Queue()
        # self.l = Queue()
        self.pool = [Thread(target=self.query) for _ in xrange(pool_size)]
        assert callable(job), 'job must be callable'
        self.job = job

    def query(self):
        while 1:
            task = self.q.get()
            if isinstance(task, int):
                time.sleep(5)
            self.job(task, self.q)
            if self.q.qsize == 0:
                break
        return 1
    #
    # def log(self):
    #     while 1:
    #         msg = self.l.get()
    #         if not msg:
    #             break
    #         print msg,

    def run(self, data):
        assert isinstance(data, Iterable), 'data is not iterable'
        # log = Thread(target=self.log)
        # log.start()
        # pdb.set_trace()
        for c in self.pool:
            c.start()
        # f = 0
        for j in data:
            # f += 1
            #if re_apply(j['title']).encode('utf-8') in d:
            #    continue
            self.q.put(j)
            #if f % 100 == 0:
            #    for _ in xrange(100):
            #        self.q.put(1)
        print 'go go go'

        for k in self.pool:
            k.join()


rus = u''.join((unichr(i) for i in range(1040, 1104)))
pattern = u'[^%s\/\.\\\ \[\]\(\)\-"!`#\+:&]' % (
    rus + string.letters + string.digits)
rules = (
    (u'ä', u'a'),
    (u'ă', u'a'),
    (u'і', u'i'),
    (u' +', u' '),
    (u'Ё', u'E'),
    (u'&amp;', u'a'),
    (u'ё', u'e'),
    (u"['’«»]", u'"'),
    (pattern, u''),
    (u'\/& +', u'/'),
    (u'\/', u''),
    (u'\\\\', u''),
    (u'"', u'`'),
    # (u'\/', u'\\\\'),
    (u'^ +', u''),
    (u' +$', u''),
)
re_rules = [(re.compile(i[0]), i[1]) for i in rules]


def re_apply(str_):
    tmp = str_
    for r, repl in re_rules:
        tmp = r.sub(repl, tmp)
        return tmp


def download(data, q):
    url = tmp = None

    try:
        path_ = [u'tmp', data['artist'].decode('utf-8')]
        path = os.path.join(*path_)
        with lock:
            if not os.path.exists(path):
                if not os.path.exists(path_[0]):
                    os.mkdir(path_[0])
                os.mkdir(path)

        try:
            url = os.path.join(u'tmp', data['artist'].decode('utf-8'), data['title'].decode('utf-8') + u'.mp3')
        except Exception as e:
            print 1
        if os.path.exists(url):
            # print 'exist song:', url
            return
        s = list(string.letters)
        random.shuffle(s)
        tmp = 'tmp_mp3_' + ''.join(s[:8])
        with lock:
            print 'get song:', type(url), url
        urllib.urlretrieve(data['url'], tmp)
        os.rename(tmp, url)
        with lock:
            print 'moved to dir', url
    except:
        traceback.print_exc()
        if url is not None and os.path.exists(url):
            os.remove(url)
        if tmp is not None and os.path.exists(tmp):
            os.remove(tmp)
        print '!!!!!!fail', data
        q.put(data)


def remove_tmp():
    import os

    for root, dirs, files in os.walk("."):
        for file_ in files:
            if file_.startswith("tmp_mp3_"):
                os.remove(file_)
            if file_.startswith(".fuse_hidd"):
                os.remove(file_)


def gettind_urls(pr=False, get_vk=False):
    remove_tmp()
    # k = ('access_token=942fa486fca9443462686cbe93176a8634a4b6aa3197b415264567cc760cd85f3c37c062a643388688128'
    #      '&expires_in=86400'
    #      '&user_id=14921565')
    print 'getting data'
    #req = urllib2.Request(
    #    u'https://api.vk.com/method/audio.get',
    #    data=urllib.urlencode({
    #        u'access_token': u'73d01e0d4800e40f691129598f24de58b87d16e52fa23aa24c2b80cc85c31bdf8ef6f25430bb329b7ec71',
    #        u'owner_id': u'14921565',
    #        u'need_user': 0})
    #)
    #resp = urllib2.urlopen(req)
    #data = resp.read()
    #resp_d = json.loads(data)

    # def dd(data):
    #     path = os.path.join('tmp', data['artist'], data['title'] + '.mp3')
    #     if len(re_apply(path)) != len(path):
    #         print type(path), path, '\n                ', re_apply(path), '\n'
    if get_vk:
        html = process()
        with open('vk_com.html', 'wb') as vk:
            vk.write(html.encode('utf-8'))
    else:
        with open('vk_com.html') as vk:
            html = vk.read().decode('utf-8')


    if pr:
        for i in parse(html):
            for j, k in i.items():
                print j, k
            print

    print 'creating treads'
    qe = TaskToThreadPool(10, download)
    print 'run download'
    qe.run(parse(html))


print 'start'
gettind_urls(get_vk=1, pr=1)


