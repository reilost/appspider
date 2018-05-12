# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 10:20
# @Author  : ddvv
# @Site    : 
# @File    : gifmakercore.py
# @Software: PyCharm

from urllib.parse import urlparse, parse_qsl
from hashlib import md5, sha256


# 第一个参数 url带参数的
# 第二个参数 表单内容去掉&sig=xxx 的
def sign_gifshow(url, form, ext=False):
    gifshow = {
        'algorithm': sign_gifshow,
        'suffix': '382700b563f4'
    }
    parsed = urlparse(url)
    params = []
    for pair in parse_qsl('{0}&{1}'.format(parsed.query, form), True):
        params.append('{0}={1}'.format(pair[0], pair[1]))
    params.sort()
    to_sign = ''.join(params)
    sig = md5((to_sign + gifshow['suffix']).encode()).hexdigest()
    signed_form = form + '&sig={0}'.format(sig)
    if (ext):
        __NStokensig = sha256((sig + '57039b18e851459c412b2265da22d2f9').encode()).hexdigest()
        signed_form = signed_form + '&__NStokensig={0}'.format(__NStokensig)
    return signed_form


def main():
    url = "http://api.gifshow.com/rest/n/feed/hot?mod=HUAWEI(HUAWEI%20NXT-AL10)&lon=0&country_code=cn&did=ANDROID_3f4f9a09bd6ea55e&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=360APP&sys=ANDROID_6.0&appver=5.4.7.5589&ftt=&language=zh-cn&iuid=&lat=0&ver=5.4&max_memory=384"
    post = "type=6&page=1&coldStart=false&count=20&pv=false&id=1&refreshTimes=1&pcursor=&client_key=3c2cd3f3&os=android"
    ret = sign_gifshow(url, post)
    print(ret)


if __name__ == "__main__":
    main()
