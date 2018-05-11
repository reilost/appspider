import time
import random
import json
import logging
from appspider.items import AppspiderItem


def getbangclelogger():
    """

    :return: 日志对象
    """
    log_format = '%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s'
    logging.basicConfig(
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    return logging.getLogger('*** BangcleSpider log ***')


# 导出该日志对象
logger = getbangclelogger()


def setbangcleitem(msg_type, data_type, data, **kwargs):
    """

    :param msg_type: message type, for example "Bangcle-0000-000"
    :param data_type: data type, for example "json"
    :param data: response data
    :param kwargs: CONST_INFO
    :return:
    """
    item = AppspiderItem()
    _rticket = int(round(time.time()))
    item['rid'] = str(_rticket) + '|' + kwargs['app_name'] + '|' + str(random.randint(100, 1000))
    item['date'] = _rticket
    item['msg_type'] = msg_type
    item['data_type'] = data_type
    for key, value in kwargs.items():
        item[key] = value
    item['data'] = json.dumps(data)

    return item
