# @Time    : 2018/8/29 下午4:43
# @Author  : 郑超
# @Desc    : selenium + web_driver
from selenium import webdriver
import json
import time


class Douyu:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get("https://www.douyu.com/directory/all")

    def get_content(self):
        time.sleep(3)
        li_list = self.driver.find_elements_by_xpath('//ul[@id="live-list-contentbox"]/li')
        contents = []
        for i in li_list:  # 遍历房间列表
            item = {}
            item["img"] = i.find_element_by_xpath("./a//img").get_attribute("src")
            item["title"] = i.find_element_by_xpath("./a").get_attribute("title")
            item["category"] = i.find_element_by_xpath("./a/div[@class='mes']/div/span").text
            item["name"] = i.find_element_by_xpath("./a/div[@class='mes']/p/span[1]").text
            item["watch_num"] = i.find_element_by_xpath("./a/div[@class='mes']/p/span[2]").text
            print(item)
            contents.append(item)
        return contents

    # 保存本地
    def save_content(self, contents):
        with open("douyu.txt", "a", encoding='utf-8')as f:
            for content in contents:
                json.dump(content, f, ensure_ascii=False, indent=2)
                f.write("\n")
        f.write(json.dumps(content, ensure_ascii=False) + "\n")

    def run(self):
        contents = self.get_content()
        self.save_content(contents)
        # 3.循环  点击下一页按钮，直到下一页对应的class名字不再是"shark-pager-next"
        while self.driver.find_element_by_class_name("shark-pager-next"):
            self.driver.find_element_by_class_name("shark-pager-next").click()
            contents = self.get_content()
            self.save_content(contents)


if __name__ == "__main__":
    douyu = Douyu()
    douyu.run()
