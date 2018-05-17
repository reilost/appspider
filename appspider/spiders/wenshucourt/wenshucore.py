# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 17:30
# @Author  : ddvv
# @Site    : 
# @File    : test_wenshu.py
# @Software: PyCharm

"""

"""

import base64
import hashlib
import random
import time
from Crypto.Cipher import AES

# v2.7a1 已经有pad方法了 Crypto.Util.Padding.pad
# 2.6.1需要自定义
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def StrToLong(s, i):
    v10 = i
    v4 = v10
    v7 = 1
    v6 = len(s)
    while v7 < v6:
        v4 += (v10 + v7 + (ord(s[v7]) << (v7 & 7)) - ord(s[v7]))
        v7 += 1
    return v4


def StrToLong2(s, i):
    v10 = i
    v4 = v10
    v7 = 1
    v6 = len(s)
    while v7 < v6:
        v4 += (v10 + v7 + (ord(s[v7]) << (v7 & 0xf)) - ord(s[v7]))
        v7 += 1
    return v4


def StrToLong3(s, i):
    v10 = i
    v4 = v10
    v7 = 1
    v6 = len(s)
    while v7 < v6:
        v4 += (v10 + v7 + (ord(s[v7]) << (v7 & 0xf)) + (v7 % 4) - ord(s[v7]))
        v7 += 1
    return v4


def calcmd5(s):
    hl = hashlib.md5()
    hl.update(s.encode())
    mymd5 = hl.hexdigest()
    return mymd5


def fun0(s):
    s2 = s[5:30] + s[36:39]
    md5 = calcmd5(s2)
    return md5[4:20]


def fun1(s):
    s2 = s[5:30] + '5' + s[1:3] + '1' + s[36:39]
    s3 = s2[4:] + (s2[5:] + s2[4:])[3:]
    md5 = calcmd5(s3)
    return md5[6:22]


def fun2(s):
    s2 = s[5:30] + s[1:3] + '1' + s[36:39]
    s3 = s2[4:] + calcmd5((s2[5:] + s2[4:])[6:])
    md5 = calcmd5(s3)
    return md5[1:17]


def fun3(s):
    s2 = s[5:30] + s[36:39]
    s3 = str(StrToLong2(s2[4:], 5)) + (s2[5:] + s2[7:])[1:]
    md5 = calcmd5(s3)
    return md5[1:17]


def fun4(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong(s2[4:], 13)) + (s2[12:] + s2[4:])[2:]
    md5 = calcmd5(s3)
    return md5[1:17]


def fun5(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong(s2[4:], 2)) + (s2[12:] + s2[4:])[2:]
    md5 = calcmd5(s3)
    return md5[3:19]


def fun6(s):
    s2 = s[2:27] + s[30:33]
    s3 = str(StrToLong2(s2[4:], 3)) + (s2[1:] + s2[4:])[2:]
    md5 = calcmd5(s3)
    return md5[10:26]


def fun7(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong3(s2[2:], 11)) + (s2[2:] + s2[6:12])[2:]
    md5 = calcmd5(s3)
    return md5[6:22]


def fun8(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong(s2[4:], 13)) + base64.b64encode((s2[12:] + s2[4:]).encode())[2:].decode()
    md5 = calcmd5(s3)
    return md5[1:17]


def fun9(s):
    s2 = s[2:27] + s[36:39]
    s3 = s2[12:] + s2[4:]
    s4 = base64.b64encode(s2[4:].encode()).decode() + s3[2:]
    md5 = calcmd5(s4)
    return md5[7:23]


def fun10(s):
    s2 = s[5:27] + s[12:15]
    md5 = calcmd5(s2)
    return md5[9:25]


def fun11(s):
    s2 = s[5:30] + '5whq' + s[1:3] + '1' + s[36:39]
    s3 = s2[4:] + (s2[10:] + s2[4:])[3:]
    md5 = calcmd5(s3)
    return md5[6:22]


def fun12(s):
    s2 = s[5:30] + s[1:3] + '1' + s[36:39]
    s3 = s2[4:] + StrToLong3((s2[5:] + s2[4:])[6:], 45)
    md5 = calcmd5(s3)
    return md5[1:17]


def fun13(s):
    s2 = s[5:30] + s[36:39]
    s3 = calcmd5(s2[4:] + '5') + (s2[5:] + s2[7:])[1:]
    md5 = calcmd5(s3)
    return md5[1:17]


def fun14(s):
    s2 = s[2:27] + s[16:19]
    s3 = str(StrToLong2(s2[4:], 2)) + (s2[12:] + s2[4:])[2:]
    md5 = calcmd5(s3)
    return md5[11:27]


def fun15(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong3(s2[4:], 2)) + (s2[12:] + s2[4:])[2:]
    md5 = calcmd5(s3)
    return md5[3:19]


def fun16(s):
    s2 = s[2:27] + s[30:33]
    s3 = str(StrToLong2(s2[4:], 1)) + base64.b64encode((s2[12:] + s2[4:])[2:].encode()).decode()
    md5 = calcmd5(s3)
    return md5[1:17]


def fun17(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong3(s2[2:], 11)) + base64.b64encode((s2[2:] + s2[6:12])[12:].encode()).decode()
    md5 = calcmd5(s3)
    return md5[3:19]


def fun18(s):
    s2 = s[2:27] + s[36:39]
    s3 = str(StrToLong(s2[4:] + 'f4v6', 13)) + base64.b64encode((s2[10:] + 'a2aaa' + s2[4:]).encode())[2:].decode()
    md5 = calcmd5(s3)
    return md5[1:17]


def fun19(s):
    s2 = s[2:27] + 'a2daa' + s[36:39]
    s3 = s2[12:] + s2[4:]
    s4 = base64.b64encode(s2[4:].encode()).decode() + s3[2:]
    md5 = calcmd5(s4)
    return md5[7:23]


funs = [fun0, fun1, fun2, fun3, fun4, fun5, fun6, fun7, fun8, fun9, fun10, fun11, fun12, fun13, fun14, fun15, fun16,
        fun17, fun18, fun19]


def getrandomchr(l):
    nonces = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(nonces)
    s = ''
    for i in range(0, l):
        s += nonces[random.randint(0, length - 1)]
    return s


def sortstring(s1, s2, s3):
    str_list = [s1, s2, s3]
    r_list = sorted(str_list)

    return ''.join(r_list)


def signature(timestamp, nonce, deviceid):
    s = sortstring(timestamp, nonce, deviceid)
    md5 = calcmd5(s)
    return md5


def decryptAES(key, ciphertext):
    iv = '909bf452b64a4cda'
    obj = AES.new(key, AES.MODE_CBC, iv)
    a = obj.decrypt(base64.b64decode(ciphertext))
    cleartext = unpad(a.decode())

    return cleartext


def gettime():
    timestamp = time.time()
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y%m%d%H%M%S", time_local)
    return dt

def main():
    # token = 'fbd9ce30a52add4664bd8ef4021c0072'
    # timestamp = '20180412200937'
    # ciphertext = 'CBE7Wozuh8KZpTIrKi9ums3C9rl0phQBr2lCosVFO6m1i8xpsQAGkhDlJdXzuLX+EqTBXfab0VoUkd2E3mXPZQo0wtnb4W/07EBavDfqvk3t0fFzv1XeuKJICb9Z15sXuj0aRhBGnBLz6zjVABVqVvi6d6UwGzflWivZk11bYv4+IHp3HB68SpFPFfaTa6tQ2rLbFgRzNdemuhcmXNDMlAni+nAlLVZ5SIxDLRre/L6DHxyiVTXkQoXDC4Bo5L677v1ecmKOajd7vwX8tsi/i76oqFf+b8Exn76ICd7fDvXSzknxah1m9b6/VA4z6d74ZxLdXkT8+T25gPUXyWjaVPiA7M++JXyz/k1+c3n7Yer3N0MQZ5kPjREfPtIbr1zyU7P9fKiN10VBjYXfh5dfgMxmBVF7eSqrUsKmB62vU7TErfiHE0rwukVdgdbhFS7aBz/35Ajz2F+VFW/iOa8XGiYkSGjzAEXs9eTAdHPohXaqj6kb4RY6Ckh2lRqLnyoqf16MzS0kV7nrcxxTOcBGjpVVG04Yob9gaGX1Q2Zs8PA1He0dgwoJgiCCVbBVW+Ofccdbhc/02ea3C8NHE1ZHeiRzWepzCedZS4ltBNjWfAUNBjY2aAGQ7hoouhZjUCVTGQUjxBpAeBUAipS91kPv1EOUis23Y3ZwUhJZ/JL/gPhxDnTig+YboovuP5qEvaKLJ8di2RjH0zUNJz45b0KLj4TXUllv6K3tRInIrWLOExo1XQC9I3eeUsBwgYlIUfFkVyqOYfgpQeQhB4Wa7+/bnXkPJFKAxLJMHUOz2sLB/0kzv+oh8lxNoqAsY6cyAS32wqf0A73FeELdxklbvfaE7/dEWHKhOUUpMNK+m9/lUSUzl6XH4XDw/WLG5injRKEoFCxrRB9qeVEOGb9lfE0LJg=='
    # key = funs[StrToLong(token, 1) % 20](token + timestamp)
    # key = '13dc84cb9b2991c4'
    # ciphertext = '+iAmeYwp+UB9VGe8ytHI3rcKQlJbBeZFDVL+BhUuj2WZlLxQW9tdlYER1OYcbhWXlYbnzUecdVMKZEH0sigVxcvS3inS2DCI39kPeXh2HGaHQqISCrRrSmHHL3eN+30WTKcdAREkVJ84EVsEEUB8e6VU2wzlRHuxnzPGiwIebuFZeclzRxttbc3qJMqgvSthba63H35s3PUDdkZHogy/NyIcbaJeJ8FYxMr4Y5g7igDegOVPljphaFQUszpZ6iMBuU2HNazeQah+rE0mxxWH9xg5vzuJjY5OZJdfDRHRikf0KtXLD/3aSQjQZ8wYXIfNQA2iSVkNhxJPkAT6k2L9CVvMBRsPBumTwkRxclCQ0SvJo82u5kpkIgy3SdswUgXr4sJUMgEZMYyaYh0lp43bvtIB+ccd15Q52frIYZn+EqraNmkQhk/57PsbXAYxVkBGDLVCcWevlz8/S1JPRw7NmoZCdCl55Ni8uA1TZ/7t2XBeDdTPHWzCyT7H/Qw1J4aupjlTj0o74b1uAy8/VpNKna/hnCfIcaDe6oPHFmlLfLKcZq4DDsgDCpCbG56g0UgWcNfiwNoq9FSpXb1uhSC8dx4mgnaLUQEmkq1lxzoop3Hs9RTkBP9FhJpro+97kpU0vabZV7aMuE4R+W27VUh7KXeWsJ7jlr/v8zleijsOcZa1efaVd+zmyaxfR9sm9yl+kUNq5JDTkSktBHehXt50XQ7j31CWDslOW5N+3MeHFrpsQFACoEHoV5ZD8Hhw8Dg689bPPHbtuiAzVH645EzQRniEzNC+xP0NtaiAuBNkEVKLADdvIYNutQV/rMwQlpCb4BW+IT3lr4DA44k+URwsIwCiwxC1plwE4+qbqCNJSeWs6k30jbK6bHgI+yOchvBn4Tir4lxCP8cD2JgYUXmX/A=='
    token = '19c9d146d7bd4ad66c91fad6861c0072'
    timestamp = '20180417143645'
    ciphertext = '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'
    key = funs[StrToLong(token, 1) % 20](token + timestamp)
    print(decryptAES(key, ciphertext))
    # print(gettime())


if __name__ == "__main__":
    main()
