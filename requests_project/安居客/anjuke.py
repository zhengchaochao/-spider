# @Time    : 2018/9/1 下午3:20
# @Author  : 郑超
# @Desc    : 安居客杭州租房信息
import json
import random, re, requests, lxml.html, csv

etree = lxml.html.etree
url_list = []
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
# 获取代理ip
rsp = requests.get(url="http://www.xicidaili.com/nn", headers=headers)
ip_html = etree.HTML(rsp.text)
b = re.findall(r'<div title=\"(.*?)秒\" class="bar"', rsp.text, re.S)

ip_list = []
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
                response = requests.get(url="https://hz.zu.anjuke.com/fangyuan/xiaoshan/p1-px7/", headers=headers, proxies=ip, timeout=10)
                if response.status_code == 200:
                    print(ip)
                    ip_list.append(ip)
            except:
                print("这个ip也太慢了吧！！！")
with open("ip.txt", "a", encoding='utf-8')as f:
    f.write(json.dumps(ip_list, ensure_ascii=False) + "\n")
print(ip_list)

for b in range(1, 200):
    dip = random.choice(ip_list)
    url = "https://hz.zu.anjuke.com/fangyuan/xiaoshan/p{}-px7/".format(b)
    print(url)
    print(dip)
    url_list.append(url)

    rsp = requests.get(url=url, headers=headers, proxies=dip)
    html = etree.HTML(rsp.text)
    name_list = []
    house_type_list = []
    position_list = []
    direction_list = []
    money_list = []
    for i in range(3, 61):
        div = html.xpath("//div[@id='list-content']/div[{}]".format(i))[0]
        name = div.xpath("./a/@title")[0]
        name_list.append(name)
        house_type = div.xpath("./div[@class='zu-info']/p[@class='details-item tag']/text()")[1] + div.xpath("./div[@class='zu-info']/p[@class='details-item tag']/text()")[2].strip()
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
    with open('安居客.csv', 'a', encoding='gbk') as f:
        writer = csv.writer(f)
        writer.writerow(['', '', '', '', ''])
        for i in item_demo:
            writer.writerow(i)
