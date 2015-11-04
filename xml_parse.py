#! -*- coding: utf-8 -*-
from lxml.html import etree

__author__ = 'vova'

from lxml.html.clean import clean_html

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr

    return start


@coroutine
def create_dict():
    r = True
    d = {}
    while r:
        dat = yield d
        if isinstance(dat, int):
            break
        a = dat.find('div/div/span/a')
        if a is not None:
            name = a.text
        else:
            name = dat.find('div/div/span').text
        d = {
            'artist': dat.find('div/div/b/a').text.encode('utf-8'),
            'url': dat.find('div/input').attrib['value'],
            'title': name.encode('utf-8'),
        }


@coroutine
def print_events(parser_, target):
    for action, element in parser_.read_events():
        print('%s: %s' % (action, element.tag))
        if (element.tag == 'div' and
                    element.attrib.get('class') == 'head2' and
                    action == 'end'):
            k = yield target.send(element)
            if k == 0:
                target.send(0)


def parse(data):
    parser = etree.HTMLPullParser(events=('start', 'end'), )
    target = create_dict()
    parser.feed(data)
    for action, element in parser.read_events():
        #print('%s: %s' % (action, element.tag))
        if element.tag == 'div' and element.attrib.get('class') == 'area clear_fix' and action == 'end':
            yield target.send(element)
    target.send(0)


# if __name__ == '__main__':
#     a = 0
#     for i in parse():
#         a += 1
#         print i
#         if a > 10:
#             break