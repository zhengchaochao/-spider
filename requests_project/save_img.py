# @Time    : 2018/9/25 下午1:51
# @Author  : 郑超
# @Desc    :

import requests

# 图片地址
img_url = "http://imglf0.nosdn.127.net/img/RWppUi92Wk1nQzFtTUtCdUdwY2Vkd1pPekVqZ1RhT0VRZVJkeFhRanc0d2Vwa2dVUmUrR25RPT0.jpg?imageView&thumbnail=500x0&quality=96&stripmeta=0&type=jpg"
img = requests.get(img_url)
f = open('test.jpg', 'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）
f.write(img.content)  # 多媒体存储content
f.close()
