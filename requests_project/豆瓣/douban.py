# @Time    : 2018/8/28 下午4:32
# @Author  : 郑超
# @Desc    : 豆瓣搜索
import time
import requests
import lxml.html
import json

etree = lxml.html.etree


# 获取页面信息
def get_url_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)["items"]


# 解析页面信息
def parse_one_page(text):
    book_list = []
    item = {}
    for _ in text:
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


# ensure_ascii=False 防止输出Unicode编码
def write_to_file(content):
    with open("result.txt", "a", encoding='utf-8')as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def run(offset):
    url = "https://www.douban.com/j/search?q=%E8%8B%8F%E8%81%94&start={}&cat=1001".format(offset)
    text = get_url_page(url)
    print(text)
    for item in parse_one_page(text):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(50):
        run(offset=i * 20)
        time.sleep(1)
