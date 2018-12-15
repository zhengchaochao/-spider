# @Time    : 2018/12/10 上午11:16
# @Author  : 郑超
# @Desc    :
import jieba, requests, random, lxml.html, urllib.parse
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from selenium import webdriver
from requests_project.ip_list import get_ip_list
from retrying import retry

etree = lxml.html.etree


class Dou:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Cookie': 'bid=awbL0uAN-7U; gr_user_id=1dc7e567-015b-4ff5-8c9e-17ed8308b278; _vwo_uuid_v2=D222C1E2EF2B02ACB213649659BE68886|2be8a86b45f3b5f2bc61d6ba5e3f67e4; push_noty_num=0; push_doumail_num=0; __yadk_uid=XIFVP83zMywGSNJJ6QCIqLr9WjihA5So; ll="118172"; _ga=GA1.2.548953649.1529479409; douban-fav-remind=1; __utmv=30149280.14521; viewed="10956502_23008813_6082808_2055664"; __utmc=30149280; dbcl2="145211630:lvWyTI1o6qg"; ck=D492; __utmc=81379588; ct=y; ap_v=0,6.0; __utma=30149280.548953649.1529479409.1544522109.1544526802.22; __utmz=30149280.1544526802.22.21.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.2051771135.1524756537.1542177124.1544526850.16; __utmz=81379588.1544526850.16.13.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1544526850%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fcat%3D1001%26q%3D%25E6%25B0%25B4%25E6%25B5%2592%25E4%25BC%25A0%22%5D; _pk_ses.100001.3ac3=*; __utmt=1; __utmt_douban=1; _pk_id.100001.3ac3=4399e9b951712a07.1524756537.17.1544528995.1542177278.; __utmb=30149280.20.10.1544526802; __utmb=81379588.12.10.1544526850'
        }
        self.book_name = input("请输入你想搜索的书名:\n")
        self.font = "./data/rain.ttf"  # 字体文件
        self.background_color = "white"
        self.width = 1000
        self.height = 800
        self.ip = random.choice(get_ip_list(url="https://book.douban.com/"))

    def get_name(self):
        """
        将中文书名转换为url
        :return:
        """
        name = urllib.parse.quote(self.book_name, "utf8")
        url = "https://book.douban.com/subject_search?search_text={}&cat=1001".format(name)
        driver = webdriver.PhantomJS()
        driver.get(url)
        try:
            div_list = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div/a').get_attribute(
                "href")
        except:
            div_list = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/a').get_attribute(
                "href")
        book_id = str(div_list).split("/")[-2]
        return book_id

    @retry(stop_max_attempt_number=5)
    def get_text(self, book_id):
        """
        获取 该书评价的文本
        :param book_id:  书籍的io
        :return:
        """
        txt_list = []
        i = 1
        while True:
            url = "https://book.douban.com/subject/{}/comments/hot?p={}".format(book_id, i)
            print(url)
            i += 1
            rsp = requests.get(url=url, headers=self.headers, proxies=self.ip)
            html = etree.HTML(rsp.text)
            if len(html.xpath('//*[@id="comments"]/ul/li[1]/div[2]/p/span//text()')) == 0:
                break
            li_list = html.xpath("//*[@id='comments']/ul/li")
            for x in li_list:
                content = x.xpath("div[2]/p/span//text()")
                txt_list.append(content)
                with open(self.book_name + '.txt', 'a', encoding='utf8') as f:
                    f.write(content[0] + "\n")
                    f.close()

    def draw_yun(self):
        """
        画出想要的云图
        :return:
        """
        img_array = np.array(Image.open("./data/timg.png"))
        text = open(self.book_name + '.txt', "r", encoding="utf8").read()
        cut = jieba.cut(text)  # 分词
        string = " ".join(cut)
        wc = WordCloud(
            font_path=self.font,
            background_color=self.background_color,
            width=self.width,
            height=self.height,
            mask=img_array
        )

        wc.generate_from_text(string)  # 绘制图片1
        plt.imshow(wc)  # 用plt显示图片
        plt.axis('off')  # 不显示坐标轴
        plt.figure()
        plt.show()  # 显示图片
        # wc.to_file('ss.png')  # 保存图片


if __name__ == '__main__':
    d = Dou()
    book_id = d.get_name()
    d.get_text(book_id)
    d.draw_yun()
