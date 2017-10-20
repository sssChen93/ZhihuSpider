# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import AccountInfoItem

import json
import re


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['https://www.zhihu.com/api/v4/members/zhu-xuan-86/followers?limit=20&offset=0']

    def parse(self, response):
        response_text = json.loads(response.text)
        match_obj = re.match(".*members/(.*?)/", response.url)
        if match_obj:
            followed = match_obj.group(1)

            account_item = AccountInfoItem()
            for single_people in response_text["data"]:
                account_item["avatar_url_template"] = single_people["avatar_url_template"]
                account_item["name"] = single_people["name"]
                account_item["headline"] = single_people["headline"]
                account_item["gender"] = single_people["gender"]
                account_item["user_type"] = single_people["user_type"]
                account_item["url_token"] = single_people["url_token"]
                account_item["is_advertiser"] = single_people["is_advertiser"]
                account_item["account_type"] = single_people["type"]
                account_item["badge"] = single_people["badge"]
                account_item["unique_id"] = single_people["id"]
                account_item["is_org"] = single_people["is_org"]
                account_item["follower"] = single_people["url_token"]
                account_item["followed"] = followed
                yield account_item
                next_url = "https://www.zhihu.com/api/v4/members/{}/followers?offset=0&limit=20"
                yield Request(url=next_url.format(single_people["url_token"]), callback=self.parse, dont_filter=True)

            if not response_text['paging']['is_end']:
                yield Request(url=response_text['paging']['next'], callback=self.parse, dont_filter=True)

