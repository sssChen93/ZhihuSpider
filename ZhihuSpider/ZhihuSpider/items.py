# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AccountInfoItem(scrapy.Item):
    avatar_url_template = scrapy.Field()  # 头像
    name = scrapy.Field()                 # 昵称
    headline = scrapy.Field()             # 签名
    gender = scrapy.Field()               # 性别
    user_type = scrapy.Field()            # 用户类型
    url_token = scrapy.Field()            # 用户token
    is_advertiser = scrapy.Field()        # 是否广告用户
    account_type = scrapy.Field()         # 账户类型
    badge = scrapy.Field()                # 徽章(优秀回答者)
    unique_id = scrapy.Field()            # 32位ID
    is_org = scrapy.Field()               # 是否是机构号

    followed = scrapy.Field()  # 被关注的人 大V
    follower = scrapy.Field()  # 关注者     小透明

    def get_insert_account_sql(self):
        insert_sql = """
            insert into account_info(avatar_url_template, name, headline, gender, user_type, url_token, is_advertiser,\
            account_type, badge, unique_id, is_org)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self["avatar_url_template"], self["name"], self["headline"], self["gender"], self["user_type"],
                  self["url_token"], self["is_advertiser"], self["account_type"], self["badge"], self["unique_id"],
                  self["is_org"])

        return insert_sql, params

    def get_insert_relation_sql(self):
        insert_sql = """insert into follow_info(followed, follower) VALUES (%s, %s)"""
        params = (self["followed"], self["follower"])

        return insert_sql, params

