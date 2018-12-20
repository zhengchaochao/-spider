# -*- coding: utf-8 -*-
import scrapy
from ..items import SunPoliticsItem

item = SunPoliticsItem()  # 实例化


class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        next_flag = True
        table = response.xpath("//table[@width='98%']")[0]
        things = table.xpath("./tr")
        for thing in things:
            item["title"] = thing.xpath("td[2]/a[2]/text()").extract_first()
            item["href"] = thing.xpath("td[2]/a[2]/@href").extract_first()
            item["number"] = thing.xpath("td[1]//text()").extract_first()
            item["hanle_state"] = thing.xpath("td[3]/span/text()").extract_first()
            item["updata_time"] = thing.xpath("td[5]/text()").extract_first()
            item["involved_department"] = thing.xpath("td[4]/text()").extract_first()
            item["content"] = thing.xpath("td[2]/a[3]/text()").extract_first()

            yield item

            if next_flag:
                self.offset += 30
                yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
