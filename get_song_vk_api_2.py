#!/usr/bin/python
#! -*- coding: utf-8 -*-
from Queue import Queue
import json
import os
import random
from threading import Thread, Lock
import traceback
import urllib
import re
import string
from collections import Iterable
import time

__author__ = 'wilfman'

lock = Lock()


class TaskToThreadPool(object):
    def __init__(self, pool_size, job=None):
        self.pool_size = pool_size
        self.q = Queue()
        self.pool = [Thread(target=self.query) for _ in xrange(pool_size)]
        assert callable(job), 'job must be callable'
        self.job = job
        self.keep_runing = True

    def query(self):
        while 1:
            if not self.keep_runing:
                if self.q.qsize() == 0:
                    break

            task = self.q.get()
            if isinstance(task, int):
                time.sleep(5)
            self.job(task, self.q)

        return 1

    def run(self, data):
        assert isinstance(data, Iterable), 'data is not iterable'

        for c in self.pool:
            c.start()

        for j in data:
            self.q.put(j)

        print 'go go go'
        self.keep_runing = False

        for k in self.pool:
            k.join()

def rules():
    rus = u''.join((unichr(i) for i in range(1040, 1104)))
    pattern = u'[^%s\/\.\\\ \[\]\(\)\-"!`#\+:&]' % (
        rus + string.letters + string.digits)
    rules_ = (
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
        (u'^ +', u''),
        (u' +$', u''),
        (u'[\ufeff]', u''),
    )
    return [(re.compile(i[0]), i[1]) for i in rules_]
re_rules = rules()

def re_apply(str_):
    tmp = str_
    for r, repl in re_rules:
        tmp = r.sub(repl, tmp)
    return tmp.lower()


def download(data, q=None):
    url = tmp = None
    data['artist'] = re_apply(data['artist'])[:50]
    data['title'] = re_apply(data['title'])[:50]
    try:
        try:
            url = os.path.join(u'tmp', data['artist'], data['title'] + u'.mp3')
        except Exception as e:
            pass

        if os.path.exists(url):
            # print 'exist song:', url
            return

        path_ = [u'tmp', data['artist']]
        path = os.path.join(*path_)
        with lock:
            if not os.path.exists(path):
                if not os.path.exists(path_[0]):
                    os.mkdir(path_[0])
                os.mkdir(path)

        s = list(string.letters)
        random.shuffle(s)
        tmp = 'tmp_mp3_' + ''.join(s[:8])
        with lock:
            print 'get song:', url
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
        if q is not None:
            q.put(data)


def remove_tmp():
    import os

    for root, dirs, files in os.walk("."):
        for file_ in files:
            if file_.startswith("tmp_mp3_"):
                os.remove(file_)
            if file_.startswith(".fuse_hidd"):
                os.remove(file_)


def parse(f_name):
    with open('erorrs.txt', 'w') as err:
        with open(f_name) as f:
            for line in f:
                if line:
                    try:
                        l = json.loads(line)
                    except:
                        print 'cannot load ', line
                        err.write(line)
                        continue
                    else:
                        yield l



def gettind_urls():
    remove_tmp()
    print 'creating treads'
    qe = TaskToThreadPool(10, download)
    print 'run download'
    qe.run(parse('vk_music.txt'))


print 'start'
gettind_urls()
