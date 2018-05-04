# -*- coding: utf-8 -*-
# @Time    : 03/04/2018 2:11 PM
# @Author  : ddvv
# @Site    :
# @File    : huaweiappstore.py
# @Software: PyCharm

import requests
import hashlib
import hmac
import base64
import gzip
import time
from os import urandom
import struct
from urllib import parse
from Crypto.Cipher import AES

# pkcs5padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

# 计算请求hash
def makeDigest(message, key):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')

    digester = hmac.new(key, message, hashlib.sha1)
    signature1 = digester.digest()
    signature2 = base64.urlsafe_b64encode(signature1)

    return str(signature2, 'UTF-8')

# 获取base64编码的iv
def codeIV():
    aArr = urandom(16)
    a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '=']
    i = len(aArr)
    i2 = 0
    new_len = int((i + 2) / 3) << 2
    new_Arr = ['0'] * new_len
    for i3 in range(0, i, 3):
        obj = None
        obj2 = None
        i4 = (aArr[i3] & 255) << 8
        if i3 + 1 < i:
            i4 |= aArr[i3 + 1] & 255
            obj = 1
        i4 = i4 << 8
        if i3 + 2 < i:
            i4 |= aArr[i3 + 2] & 255
            obj2 = 1
        new_Arr[i2 + 3] = a[i4 & 63 if obj2 is not None else 64]
        i5 = i4 >> 6
        new_Arr[i2 + 2] = a[i5 & 63 if obj is not None else 64]
        i4 = i5 >> 6
        new_Arr[i2 + 1] = a[i4 & 63]
        new_Arr[i2] = a[(i4 >> 6) & 63]
        i2 += 4
    return ''.join(new_Arr)

# 计算用户Id
def encryptUserId(iv):
    imei = '863336037384660'
    key = '-7309123397409057493'
    data = pad(imei)
    obj = AES.new(key[0:16].encode(), AES.MODE_CBC, iv)
    a = obj.encrypt(data.encode())
    xx = ""
    for x in a:
        s = hex(x & 255)
        s = s.replace('0x', '')
        if len(s) == 1:
            s = '0' + s
        xx += s
    return xx.upper()

# GZIP 解压
def GZipDecode():
    # 解压
    # huawei.data.data : 保存在文件中的，压缩后的body数据
    for i in range(1, 13):
        with gzip.open('huawei/huawei' + str(i), 'rb') as f:
            file_content = f.read()
        data = file_content.decode()
        print(data)

def sendBurpData():
    url = 'http://hispaceclt.hicloud.com/hwmarket/api/storeApi2'
    header = {
        'Content-Type': 'application/x-gzip',
        'Content-Encoding': 'gzip',
        'Host': 'hispaceclt.hicloud.com',
        'Connection': 'close',
        'User-Agent': 'HiSpace_7.0.3.302_HUAWEI'
    }
    for i in range(1, 13):
        with open('huawei/huawei' + str(i), 'rb') as f:
            data = f.read()
            rs = requests.post(url=url, headers=header, data=data)
            print(rs.text)

def testF():
    iv = parse.unquote('D%2BvrEM7b58U0n0fNfWmSVA%3D%3D')
    print(encryptUserId(base64.b64decode(iv)))

def main():
    post_data = 'accountId=220086000132592687&appid=C10101754&clientPackage=com.huawei.appmarket&cno=4010001' \
                '&code=0200&hcrId=85F366EAD2EF45EBAD825D08A9F37B30&isOwnComment={isOwnComment}&iv={iv}&maxResults={' \
                'maxResults}&method=client.user.commenList3&net=1&reqPageNum={page}&salt={' \
                'salt}&serviceType=0&sign=c9dm1001cx10010020008000000%4085F366EAD2EF45EBAD825D08A9F37B30&ts={' \
                'ts}&userId={userId}&ver=1.1'
    hmacsha_key = '-1903256023350232123'
    url = 'http://hispaceclt.hicloud.com/hwmarket/api/storeApi2'
    header = {
        'Content-Type': 'application/x-gzip',
        'Content-Encoding': 'gzip',
        'Host': 'hispaceclt.hicloud.com',
        'Connection': 'close',
        'User-Agent': 'HiSpace_7.0.3.302_HUAWEI'
    }
    for page in range(1, 13):
        ts = int(round(time.time() * 1000))
        iv = codeIV()
        uiv = parse.quote(iv)
        userid = encryptUserId(base64.b64decode(iv))
        salt = struct.unpack("<q", urandom(8))[0]
        data = post_data.format(page=page, isOwnComment=0, salt=salt, ts=ts, userId=userid, iv=uiv, maxResults=12)
        nsp_key = parse.quote(makeDigest(data, hmacsha_key))
        data += ('&nsp_key=' + nsp_key)
        # print(data)
        en_data = gzip.compress(data.encode())
        print('--------------------请求第%d页--------------------' % page)
        print('请求数据：')
        print(data)
        rs = requests.post(url=url, headers=header, data=en_data)
        print('返回数据：')
        print(rs.text)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
    # GZipDecode()
    # sendBurpData()
    # testF()