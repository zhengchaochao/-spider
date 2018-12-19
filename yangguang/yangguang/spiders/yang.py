# -*- coding: utf-8 -*-
import scrapy


class YangSpider(scrapy.Spider):
    name = 'yang'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        next_flag = True
        table = response.xpath("//table[@width='98%']")[0]
        things = table.xpath("./tr")
        for thing in things:
            title = thing.xpath("td[2]/a[2]/text()").extract_first()
            href = thing.xpath("td[2]/a[2]/@href").extract_first()
            number = thing.xpath("td[1]//text()").extract_first()
            hanle_state = thing.xpath("td[3]/span/text()").extract_first()
            updata_time = thing.xpath("td[5]/text()").extract_first()
            involved_department = thing.xpath("td[4]/text()").extract_first()
            content = thing.xpath("td[2]/a[3]/text()").extract_first()
            item = dict(
                title=title,
                href=href,
                number=number,
                hanle_state=hanle_state,
                updata_time=updata_time,
                involved_department=involved_department,
                content=content
            )
            yield item

            if next_flag:
                self.offset += 30
                yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
