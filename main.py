from multiprocessing.dummy import Pool as Threadpool
from urllib import parse

import requests

#  001 ~ 821
tmp = parse.quote('玄幻奇幻/庆余年_秋水雁翎')
target_url = [
    'http://mp3f.ting89.com:9090/' + tmp + '/%s.mp3' % str(i + 1).zfill(3)
    for i in range(821)
]

PATH = '/Users/xxx/Downloads/庆余年语音小说/'


def download(url):
    res = requests.get(url, stream=False)
    with open(PATH + url.split('/')[-1], "wb") as f:
        f.write(res.content)
    print(url.split('/')[-1])


th = Threadpool(20)

th.map(download, [i for i in target_url])
