# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 9:44
# @Author  : ddvv
# @Site    : 
# @File    : miaopaicore.py
# @Software: PyCharm

import struct
import hashlib

def decodeData(data):
    data_len = len(data)
    if data_len < 2 :
        return ''
    f1 = struct.unpack('<I', data[0:4])[0]
    f2 = struct.unpack('<I', data[4:8])[0]
    migc = f1 ^ f2
    if migc != 0x8C8BBAD3:
        return ''
    result = ''
    for i in range(8, data_len - 4, 4):
        a = struct.unpack('<I', data[i:i+4])[0]
        b = struct.unpack('<I', data[i+4:i+8])[0]
        c = hex(a ^ b)
        for j in range(len(c) - 2, 0, -2):
            result += chr(int(c[j:j+2],16))

    index = result.rfind('}')
    return result[:index+1]

def sign(path, uuid, timestamp):
    m = hashlib.md5()
    key = '4O230P1eeOixfktCk2B0K8d0PcjyPoBC'
    version = '6.7.51'
    str_encode = 'url={path}unique_id={uuid}version={version}timestamp={timestamp}{key}'.format(path=path,uuid = uuid, version=version, timestamp=timestamp, key=key)
    m.update(str_encode.encode('utf-8'))
    return m.hexdigest()

def main():
    with open('miaopaipinglun', 'rb') as f:
        data = f.read()
    print(decodeData(data))


if __name__ == "__main__":
    main()