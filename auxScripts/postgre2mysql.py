# -*- coding: utf-8 -*-
# @Time    : 29/01/2018 11:00 AM
# @Author  : ddvv
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import asyncio
import asyncpg
import pymysql
from auxScripts.setItems import *
from auxScripts.common import *
from donotpush.SQLConfigs import *

repeat_record = []
with open('share_url.json', 'r') as f:
    txt = f.read()
    if len(txt) != 0:
        repeat_record = json.loads(txt)

def transferItem(items, cols):
    global  repeat_record
    values = []
    for item in items:
        value = []
        if item['share_url'] in repeat_record:
            continue
        for col in cols:
            value.append(item[col])
        repeat_record.append(item['share_url'])
        values.append(value)
    return values


def initMysql(conn, cur, table_name):
    select_sql = 'select column_name from Information_schema.columns where table_name="{table_name}"'.format(
        table_name=table_name)
    cur.execute(select_sql)
    conn.commit()
    columns = cur.fetchall()
    columns_name = [x[0] for x in columns]
    del [columns_name[0]]
    # mysql executemany函数只能接受 %s的格式化参数，但是不管是什么类型，最后都会保存回去，主要依据表的格式。
    col_types = ['%s'] * len(columns_name)
    str_columns_type = ','.join(col_types)
    return columns_name, str_columns_type


async def run():
    postgresql_conn = await asyncpg.connect(**postgresql_config)
    mysql_conn = pymysql.connect(**local_mysql_config)
    mysql_cur = mysql_conn.cursor()
    postgresql_table = 'douyinspider'
    mysql_table = 'douyinspider'
    columns, str_columns_type = initMysql(mysql_conn, mysql_cur, mysql_table)
    # 避免有些字段是关键字，加上 ` 符号
    str_columns = '`,`'.join(columns)
    str_columns = '`' + str_columns + '`'
    mysql_sql = 'insert into {table_name}({columns}) values ({columns_type})'.format(table_name=mysql_table,
                                                                                     columns=str_columns,
                                                                                     columns_type=str_columns_type)
    dlt = 500
    begin = 0
    # end = begin + 100 * dlt
    end = 853753
    for i in range(begin, end, dlt):
        postgresql_sql = 'select * from {table_name} where id >= {min} and id < {max}'.format(
            table_name=postgresql_table, min=i, max=i + dlt)
        values = await postgresql_conn.fetch(postgresql_sql)
        values = [json.loads(value['response']) for value in values]
        try :
            for value in values:
                try:
                    if 3 == value:
                        if 'aweme_list' not in value['message']['category_list'].keys():
                            continue
                        items = setItems(columns, value['message']['category_list']['aweme_list'])
                    else:
                        if 'aweme_list' not in value['message'].keys():
                            continue
                        items = setItems(columns, value['message']['aweme_list'])
                    insert_values = transferItem(items, columns)
                    mysql_cur.executemany(mysql_sql, insert_values)
                except Exception as e:
                    logger.error(str(e))
            mysql_conn.commit()
            logger.info('index: %d' % i)
        except Exception as e:
            logger.error(str(e))
            break

    with open('share_url.json', 'w') as f:
        f.write(json.dumps(repeat_record))
    await postgresql_conn.close()
    mysql_cur.close()
    mysql_conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
