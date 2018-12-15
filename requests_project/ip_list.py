# @Time    : 2018/12/15 下午11:38
# @Author  : 郑超
# @Desc    : 获取西刺代理的ip列表
import re
import requests
import lxml.html

etree = lxml.html.etree


def get_ip_list(url):
    ip_list = []
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    # 获取代理ip
    rsp = requests.get(url="http://www.xicidaili.com/nn", headers=headers)
    ip_html = etree.HTML(rsp.text)
    for x in range(2, 103):
        tr_list = ip_html.xpath("//table[@id='ip_list']/tr[{}]".format(x))
        for tr in tr_list:
            ip_host = tr.xpath("./td[2]/text()")[0]
            ip_port = tr.xpath("./td[3]/text()")[0]
            http_type = tr.xpath("./td[6]/text()")[0]
            time = float(re.findall(r'<div title=\"(.*?)秒\" class="bar"', rsp.text, re.S)[(x - 2) * 2])
            ip = {"http": "http://" + str(ip_host) + ":" + str(ip_port)}
            if http_type == "HTTP" and time <= 1:
                try:
                    response = requests.get(url=url, headers=headers,
                                            proxies=ip, timeout=10)
                    if response.status_code == 200:
                        ip_list.append(ip)
                except:
                    print("这个ip也太慢了吧！！！")
    print(ip_list)
    return ip_list
