# @Time    : 2018/9/1 下午3:20
# @Author  : 郑超
# @Desc    : 安居客杭州租房信息
import random, requests, lxml.html, csv
from requests_project.ip_list import get_ip_list

etree = lxml.html.etree


class Anjuke:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.ip = random.choice(get_ip_list(url="https://hz.zu.anjuke.com/fangyuan/xiaoshan/p1-px7/"))

    def get_text(self):
        """
        拿取房源信息
        :return: 信息列表
        """
        name_list = []
        house_type_list = []
        position_list = []
        direction_list = []
        money_list = []
        for i in range(1, 200):
            url = "https://hz.zu.anjuke.com/fangyuan/xiaoshan/p{}-px7/".format(i)
            print(url)

            rsp = requests.get(url=url, headers=self.headers, proxies=self.ip)
            html = etree.HTML(rsp.text)
            for i in range(3, 61):
                div = html.xpath("//div[@id='list-content']/div[{}]".format(i))[0]
                name = div.xpath("./a/@title")[0]
                name_list.append(name)
                house_type = div.xpath("./div[@class='zu-info']/p[@class='details-item tag']/text()")[1] + \
                             div.xpath("./div[@class='zu-info']/p[@class='details-item tag']/text()")[2].strip()
            house_type_list.append(house_type)
            c = div.xpath("./div[@class='zu-info']/address[@class='details-item']//text()")
            position = [c[1] + c[2].strip() if len(c) > 2 else c][0]
            position_list.append(position)
            a = div.xpath("./div[@class='zu-info']/p[2]//text()")
            direction = [a[1] + a[3] + a[5] if len(a) > 5 else a[1] + a[3]][0]
            direction_list.append(direction)
            money = div.xpath("./div[@class='zu-side']//text()")[1] + div.xpath("./div[@class='zu-side']//text()")[2]
            money_list.append(money)
        item_demo = list(zip(name_list, house_type_list, position_list, direction_list, money_list))
        return item_demo

    def writer_csv(self, text_list):
        with open('安居客.csv', 'a', encoding='gbk') as f:
            writer = csv.writer(f)
            writer.writerow(['', '', '', '', ''])
            for i in text_list:
                writer.writerow(i)


if __name__ == '__main__':
    a = Anjuke()
    text = a.get_text()
    a.writer_csv(text)
