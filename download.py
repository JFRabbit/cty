import os
from multiprocessing.dummy import Pool as Threadpool

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = 'https://www.biqumo.com'
TARGET_URL = '/8_8521/'

TEMPLATE = '''<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>庆余年小说</title>
    <style type="text/css">
      #root{
        width: 1200px;
        margin: 0 auto;
      }
      #content{
        background-color: #C7EDCC;
        font-size: 72px;
      }
    </style>
  </head>
  <body>
    <div id='root'>
      <h1>%s</h1>
      %s
    </div>
  </body>
</html>'''

res_base = requests.get(BASE_URL + TARGET_URL)

soup_base = BeautifulSoup(res_base.content, "html.parser", from_encoding="utf-8")

soup = None

PATH = '/Users/jasonzhang/Desktop/庆余年小说'

target = []
num = 1
for dd in soup_base.find('dt', text='《庆余年》正文卷').next_siblings:

    if isinstance(dd, Tag):
        target.append(
            {
                'path':  PATH + '/%d %s.html' % (num, dd.a.next),
                'url':   BASE_URL + dd.a['href'],
                'title': dd.a.next
            }
        )
        num += 1


def download(kwargs):
    path = kwargs['path']
    if os.path.exists(path):
        return

    res = requests.get(kwargs['url'])
    soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")

    value = TEMPLATE % (kwargs['title'], soup.find('div', id='content').__str__().split('http')[0])
    with open(path, 'w') as f:
        f.write(value)

    print(kwargs['title'])


th = Threadpool(20)

th.map(download, target)
