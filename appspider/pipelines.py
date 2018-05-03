# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import asyncpg
import asyncio
import copy
from appspider.configs.postgreconfig import *


class AppspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class PostgreSQLPipeline(object):
    def __init__(self):
        """

        """
        self.sql_create_table = ''
        self.sql_insert_item = ''
        self.conn = None
        self.buffer = {}

        self.items_cache = []
        self.cache_threshold = 0

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        if self.conn is None:
            return

        self.items_cache.append((json.dumps(dict(item)),))

        if len(self.items_cache) > self.cache_threshold:
            rows = copy.deepcopy(self.items_cache)
            self.items_cache.clear()

            # async insert.
            asyncio.get_event_loop().run_until_complete(self.flush_rows(rows))

    def open_spider(self, spider):
        """

        :param spider:
        """
        # 这里的sql 语句不区分大小写，如果用大写字母命名表名会报错
        self.sql_insert_item = f'''INSERT INTO {spider.name.lower()}(data) VALUES
                                    ($1)
                                    ON CONFLICT DO NOTHING;
                                    '''
        self.sql_create_table = f'''CREATE TABLE IF NOT EXISTS {spider.name.lower()} (
                      "id" serial PRIMARY KEY NOT NULL,
                      "data" json NOT NULL);
                       '''
        asyncio.get_event_loop().run_until_complete(self.connect_database())
        asyncio.get_event_loop().run_until_complete(self.create_table())

    def close_spider(self, spider):
        """

        :param spider:
        """
        for queue in self.buffer.values():
            queue.cleanup()

    async def connect_database(self):
        """

        """
        self.conn = await asyncpg.connect(**postgre_configs)

    async def create_table(self):
        """

        """
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.execute(self.sql_create_table)
        except Exception:
            await tr.rollback()
            raise
        finally:
            await tr.commit()

    async def flush_rows(self, rows):
        """

        :param rows:
        """
        tr = self.conn.transaction()
        await tr.start()
        try:
            await self.conn.executemany(self.sql_insert_item, rows)
        except Exception:
            await tr.rollback()
            raise
        finally:
            await tr.commit()