# @Time    : 2018/12/16 上午12:55
# @Author  : 郑超
# @Desc    : 获取问题下的 回答并保存
import json

import requests, random
import lxml.html
from requests_project.ip_list import get_ip_list

etree = lxml.html.etree


class zhihu:
    def __init__(self):
        self.headers = {
            'cookie': '_zap=1c030852-2875-4150-ba9a-738b89ad15c0; d_c0="AACkWRKMqQ2PTvVM6_Pj6Gbp4jYV-rYJXcA=|1527496416"; '
                      '_ga=GA1.2.1263874122.1526883648; _xsrf=v3JU3S1SjI7qHteZIQ3O3JZJfvAfioJ0; tst=r; z_c0="2|1:0|10:1539255398|4:z_c0|92:Mi4xUW8xS0FnQUFBQUFBQUtSWkVveXBEU1lBQUFCZ0FsVk5abnFzWEFETmw0OEJGdXgxS3RlN2kxWTRIdVhfVEhCR0JB|33608241fb7991d646961be246e7a5b7d6bc9aa7a0877501cdc7732a2b035fe6"; __utmz=155987696.1540387419.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __gads=ID=0ef8ab9def624d22:T=1540535244:S=ALNI_MboPPSeVkJzUyyCxKzyDG4XA4P5mQ; __utma=155987696.1263874122.1526883648.1540387419.1542607028.2; __utmc=155987696; q_c1=156327d287f843c18c9d25853fa0ec5e|1543230616000|1523279051000; tgw_l7_route=bc9380c810e0cf40598c1a7b1459f027',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        # self.ip = random.choice(get_ip_list(url="https://www.zhihu.com/"))

    def get_text(self):
        contents = []
        url = "https://www.zhihu.com/question/263953798"
        rsp = requests.get(url=url, headers=self.headers)
        html = etree.HTML(rsp.text)
        div_list = html.xpath('//*[@id="QuestionAnswers-answers"]/div/div/div[2]/div/div')
        print(html.xpath('//*[@id="QuestionAnswers-answers"]/div/div/div[2]/div/div[3]/div/div[2]/div[1]/span//text()'))
        for i in div_list:
            item = {}
            item["name"] = i.xpath('div/div[1]/div[1]/div/div[1]/span//text()')
            item["content"] = i.xpath('div/div[2]/div[1]/span//text()')
            print(item)
            contents.append(item)
        return contents
        # //*[@id="QuestionAnswers-answers"]/div/div/div[2]/div/div[1]/div/div[2]/div[1]/span


    # 保存本地
    def save_content(self, contents):
        with open("zhihu.txt", "a", encoding='utf-8')as f:
            for content in contents:
                json.dump(content, f, ensure_ascii=False, indent=2)
                f.write("\n\n\n")


if __name__ == '__main__':
    z = zhihu()
    b = z.get_text()
    z.save_content(contents=b)

