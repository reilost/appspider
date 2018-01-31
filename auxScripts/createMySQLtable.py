# -*- coding: utf-8 -*-
# @Time    : 31/01/2018 2:32 PM
# @Author  : ddvv
# @Site    : 
# @File    : createMySQLtable.py
# @Software: PyCharm


from sys import argv,path
# 真尼玛蛋疼，在命令行执行时，搜索路径不全面，不增加根路径，就没法导入自定义的包
path.append('..')
import pymysql
from flatten_json import flatten
from auxScripts.common import logger, readFiles
from donotpush.SQLConfigs import *

# 根据模板创建数据库表
def createTableSQL(template_json_file, tablename):
    js = readFiles(template_json_file)
    tmplate_js = flatten(js)
    keys = sorted(tmplate_js.keys())
    sql_tmp = '`{name}` {type} NULL,\n'
    table_sql = 'CREATE TABLE `{table}` (\n`ddvv_id` INT NOT NULL AUTO_INCREMENT,\n'.format(table=tablename)
    for key in keys:
        value = tmplate_js[key]
        tmp_sql = ''
        if isinstance(value, str):
            if 0 < len(value) < 48:
                tmp_sql = sql_tmp.format(name=key, type='VARCHAR(128)')
            else:
                tmp_sql = sql_tmp.format(name=key, type='VARCHAR(512)')
        elif isinstance(value, int):
            if value > 9999999999:
                tmp_sql = sql_tmp.format(name=key, type='BIGINT UNSIGNED')
            else:
                tmp_sql = sql_tmp.format(name=key, type='INT UNSIGNED')
        elif isinstance(value, bool):
            tmp_sql = sql_tmp.format(name=key, type='TINYINT')
        else:
            logger.error(type(value))
        table_sql += tmp_sql
    table_sql += 'PRIMARY KEY (`ddvv_id`));'
    return table_sql

def main():
    try:
        mysql_conn = pymysql.connect(**local_mysql_config)
        mysql_cur = mysql_conn.cursor()
        if 3 != len(argv):
            print('请设置模板文件和将要创建的数据表名称')
            logger.error('请设置模板文件和将要创建的数据表名称')
            exit(0)
        createtable = createTableSQL(argv[1], argv[2])
        mysql_cur.execute(createtable)
        mysql_conn.commit()
        mysql_cur.close()
        mysql_conn.close()
        logger.info('%s create success.' % argv[2])
    except Exception as e:
        logger.error(str(e))

if __name__ == "__main__":
    main()