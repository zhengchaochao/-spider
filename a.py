# @Time    : 2018/12/19 下午4:09
# @Author  : 郑超
# @Desc    :

import requests
import lxml.html

etree = lxml.html.etree
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36',
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Accept-Encoding": "gzip, deflate",
    'Cookie': 'PHPSESSID=8iloghdkdkp3i1l9dgq3g68451; PHPSESSID_NS_Sig=oenCV6mfkWd8uVC7; PHPStat_First_Time_10000001=1545202629075; PHPStat_Cookie_Global_User_Id=_ck18121914570910828207466608233; PHPStat_Return_Time_10000001=1545202629075; NSC_wt_xa.tvo0769.dpn=ffffffffc3a0145d45525d5f4f58455e445a4a423660; PHPStat_Msrc_10000001=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; PHPStat_Msrc_Type_10000001=pmf_from_free_search'
}

rsp = requests.get(url="http://wz.sun0769.com/index.php/question/questionType?type=4&page=1", headers=headers)
rsp.encoding = 'GBK'
html = etree.HTML(rsp.text)
table = html.xpath("//table[@width='98%']")[0]
things = table.xpath("./tr")
print(things)
for thing in things:
    print("*"*80)
    title = thing.xpath("td[2]/a[2]/text()")
    href = thing.xpath("td[2]/a[2]/@href")
    number = thing.xpath("td[1]//text()")
    hanle_state = thing.xpath("td[3]/span/text()")
    updata_time = thing.xpath("td[5]/text()")
    involved_department = thing.xpath("td[4]/text()")
    content = thing.xpath("td[2]/a[3]/text()")
    print(title,href,number,hanle_state,updata_time,involved_department,content)
