# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import pymysql

class ZhihuPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self, dbparms):
        self.conn = pymysql.connect(dbparms['host'], dbparms['user'], dbparms['passwd'], dbparms['db'],
                                    charset=dbparms['charset'], use_unicode=dbparms['use_unicode'])
        self.cursor = self.conn.cursor()

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            use_unicode=True,
        )
        return cls(dbparms)

    def process_item(self, item, spider):
        try:
            insert_sql = """
                insert into account_info(avatar_url_template, name, headline, gender, user_type, url_token, is_advertiser,\
                account_type, badge, unique_id, is_org)\
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """ .format(item["avatar_url_template"], item["name"], item["headline"], item["gender"], item["user_type"],
                      item["url_token"], item["is_advertiser"], item["account_type"], item["badge"], item["unique_id"],
                      item["is_org"])
            # print(insert_sql)
            self.cursor.execute(insert_sql)
            self.conn.commit()

        except Exception as e:
            print(e)

        try:
            params = (item["followed"], item["follower"])
            insert_sql = """insert into follow_info(followed, follower) VALUES ('%s', '%s')""" % params
            # print(insert_sql)
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            print(e)


    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbparms = dict(
    #         host=settings["MYSQL_HOST"],
    #         db=settings["MYSQL_DBNAME"],
    #         user=settings["MYSQL_USER"],
    #         passwd=settings["MYSQL_PASSWORD"],
    #         charset='utf8',
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
    #
    #     return cls(dbpool)
    #
    # def process_item(self, item, spider):
    #     # 使用twisted将mysql插入变成异步执行
    #     query = self.dbpool.runInteraction(self.do_insert, item)
    #     query.addErrback(self.handle_error, item, spider)  # 处理异常
    #
    # def handle_error(self, failure, item, spider):
    #     # 处理异步插入的异常
    #     print(failure)
    #
    # def do_insert(self, cursor, item):
    #     # 执行具体的插入
    #     # 根据不同的item 构建不同的sql语句并插入到mysql中
    #     insert_sql, params = item.get_insert_account_sql()
    #     cursor.execute(insert_sql, params)
    #     insert_sql, params = item.get_insert_relation_sql()
    #     cursor.execute(insert_sql, params)
    #     pass


