import requests
from lxml import etree
import re
import mysql.connector
from helper import MySqlHelper

#去掉特殊符号
import re
def clean_text(text):
    text = re.sub(r'[\r\n\t\xa0]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\ue000-\uf8ff]', '', text)  
    text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
    return text.strip()

#发送给谁
url = 'https://www.baidu.com/'

#伪装自己
#右键，检查（N）, network，找到user-agent
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}


#发送请求
response = requests.get(url,headers=headers)

#设置编码（防止乱码）
response.encoding = 'utf-8'

#响应信息
e = etree.HTML(response.text)
lis = e.xpath('//ul[contains(@class,"s-hotsearch-content")]/li')
items = []
for li in lis:
    text = ''.join(li.xpath('.//a//text()'))
    text = clean_text(text)
    if text:
        items.append(text)

def first_digit(title):
    m = re.match(r'(\d)', title)
    return int(m.group(1)) if m else 999

titles = [re.sub(r'^[0-9]', '', t).strip() for t in items]

#print(titles)
#保存
with open('百度热搜.txt', 'w', encoding='utf-8') as f:
    for i, t in enumerate(titles, 1):
        print(f"{i:2}. {t}")
        f.write(f"{i:2}. {t}\n")

#写入数据库
db = MySqlHelper("localhost","root","123456","test")
db.connect()
for i, t in enumerate(titles, 1):
    db.add(
        table="hotsearch",
        columns=["id", "hot_rank", "entry"],
        values=(i, i-1, t)
    )

db.close()