from requests_html import HTMLSession
import pandas as pd
import json

url = "https://ecshweb.pchome.com.tw/search/v3.3/all/category/DXBJ/results?"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"}

raw_data = []
for i in range(1, 42):
    session = HTMLSession()
    payload = {"q": "輪胎", "page": i, "sort": "sale/dc"}
    res = session.get(url, params=payload, headers=headers)
    data = res.json()["prods"]
    raw_data.append(data)

df = pd.DataFrame(columns=['Id', 'cateId', 'picS', 'picB', 'name', 'describe', 'price', 'originPrice', 'author', 'brand', 'publishDate', 'sellerId', 'isPChome', 'isNC17', 'couponActid', 'BU'])
for d in raw_data:
    for x in d:
        df = df.append(x, ignore_index=True)

print(df)

df.to_csv("/Users/kai/Desktop/pchome輪胎價格.csv", index=False)
