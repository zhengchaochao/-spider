# @Time    : 2018/9/26 下午4:06
# @Author  : 郑超
# @Desc    :
import requests
import lxml.html
import json
from requests_project.douban.MySQLCommand import MySQLCommand

etree = lxml.html.etree


class D_book:
    def __init__(self):
        self.url_temp = "https://www.douban.com/j/search?q=%E8%8B%8F%E8%81%94&start={}&cat=1001"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

    # 获取url列表
    def get_url_list(self):
        return [self.url_temp.format(i * 10) for i in range(1,2)]

    def parse_url(self, url):
        print(url)
        return json.loads(requests.get(url=url, headers=self.headers).text)["items"]

    def get_content_list(self, html_str):
        book_list = []
        item = {}
        print(html_str)
        print(len(html_str))
        for _ in html_str:
            html = etree.HTML(_)
            item["name"] = html.xpath("//div[@class='pic']//a/@title")
            item["pic"] = html.xpath("//div[@class='pic']//a/img/@src")
            item["score"] = html.xpath("//div[@class='content']//span[@class='rating_nums']//text()")
            item["evaluate"] = html.xpath("//div[@class='content']//div[@class='rating-info']/span[3]/text()")
            item["author"] = html.xpath("//div[@class='content']//span[@class='subject-cast']/text()")
            item["content"] = html.xpath("//div[@class='content']/p//text()")
            item_demo = list(zip(item['name'], item['pic'], item['score'], item['evaluate'], item['author'], item['content']))
            if len(item_demo) > 0:
                book_list.append(item_demo[0])
        return book_list

    def save_content_list(self, book_list):
        # 连接数据库
        mysqlCommand = MySQLCommand()
        mysqlCommand.connect_mysql()
        # 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
        # dataCount = int(mysqlCommand.get_last_id()) + 1
        for book in book_list:  # 遍历列表，获取有效信息
            # 把爬取到的每条数据组合成一个字典用于数据库数据的插入
            my_dict = {"book_name": str(book[0]), "book_img": str(book[1]), "score": str(book[2]), "people_num": str(book[3]), "author": str(book[4]), "abstract": str(book[5])}
            try:
                # 插入数据，如果已经存在就不在重复插入
                res = mysqlCommand.insert_data(my_dict)
                if res:
                    dataCount = res
            except Exception as e:
                print("插入数据失败", str(e))  # 输出插入失败的报错语句
        mysqlCommand.close_mysql()  # 最后一定要要把数据关闭

    def run(self):
        # 获取url列表
        url_list = self.get_url_list()
        # 遍历，发送请求
        for url in url_list:
            html_str = self.parse_url(url=url)
            book_list = self.get_content_list(html_str=html_str)
            # 保存
            self.save_content_list(book_list=book_list)


if __name__ == '__main__':
    a = D_book()
    a.run()
