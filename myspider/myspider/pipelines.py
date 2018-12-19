# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        with open("team.txt", "a") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)