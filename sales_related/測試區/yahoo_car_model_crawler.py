from requests_html import HTMLSession
from time import sleep
from random import randint
import csv
from datetime import datetime
from selectolax.parser import HTMLParser
import requests
import pandas as pd
import warnings
import time

warnings.filterwarnings("ignore")


class YahooCarCrawler:
    with open("user_agent.text") as f:
        user_agent_list = [line.rstrip("\n") for line in f]

    def __init__(self, start_year=2012):
        self.start_page = "https://autos.yahoo.com.tw/new-cars/research/"
        self.df = pd.DataFrame(columns=["年份", "品牌", "車系", "車型", "價格", "動力型式", "排氣量", "驅動型式", "輪胎尺碼", "車身型式", "車重"])
        self.year = int(start_year)

    def random_header(self):
        random_agent = self.user_agent_list[randint(0, len(self.user_agent_list) - 1)]
        headers = {"User-Agent": random_agent, }
        return headers

    def get_brands_sites(self):
        res = requests.get(self.start_page, headers=self.random_header())
        parser = HTMLParser(res.text)
        brand_links = [brand.css_first("a.gabtn").attributes["href"] for brand in parser.css("div.list")]
        print(brand_links)
        return brand_links

    def get_all_models(self, links=[]):
        models = []
        n_session = HTMLSession()
        for link in links:
            response = n_session.get(link, headers=self.random_header())
            # render裡面需要有parameters，sleep讓他有時間可以讀取，scrolldown模擬滑鼠要往下拉多少
            response.html.render(sleep=1, keep_page=True, scrolldown=20)
            for r in response.html.find("div.make-main.jq-make-wrapper > div:nth-child(n+3) > a.gabtn"):
                if int(r.attrs["href"][-4:]) >= self.year:
                    models.append(r.attrs["href"])
                    print(r.attrs["href"])
                    with open("all_model_links.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([r.attrs["href"].strip()])
        sleep(randint(0, 1))
        # print(len(models))
        return models

    def all_car_links(self, source=[]):
        cars = []
        for car in source:
            response = requests.get(car, headers=self.random_header())
            parser = HTMLParser(response.text)
            mobiles = parser.css("div.body-wrapper > div.main > div.main-model > div.model-wrapper > ul > a")
            for mobile in mobiles:
                base_url = mobile.attributes["href"].strip()
                url = base_url + "/spec"
                with open("all_spec_links.csv", "a", newline="") as spec:
                    writer = csv.writer(spec)
                    writer.writerow([url])
                print(url)
                cars.append(url)
                res = requests.get(url, headers=self.random_header())
                try:
                    for data in res.iter_content(chunk_size=1024):
                        data
                except:
                    print("Failed")
                    pass
                else:
                    parser = HTMLParser(res.text)
                    values = parser.css("div.body-wrapper > div.main > div.trim-main > div.trim-spec-detail > div:nth-child(1) > ul > li > span:nth-child(2n)")
                    keys = parser.css("div.body-wrapper > div.main > div.trim-main > div.trim-spec-detail > div:nth-child(1) > ul > li > span:nth-child(2n-1)")
                    target_info = ["動力型式", "排氣量", "驅動型式", "輪胎尺碼", "車身型式", "車重"]
                    info_dict = dict()
                    for key, value in zip(keys, values):
                        # print(key.text(), value.text())
                        if key.text().strip() in target_info:
                            info_dict.setdefault(key.text().strip(), value.text().strip())
                    result = list(info_dict.values())
                    print(result)
                    if "排氣量" not in info_dict.keys():
                        result.insert(1, "NA")
                    if "車重" not in info_dict.keys():
                        result.append("NA")
                    try:
                        brand = parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(5)").text()
                    except:
                        brand = "NA"
                    try:
                        year = \
                            parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(7)").attributes[
                                "title"][0:4]
                    except:
                        year = "NA"
                    try:
                        series = \
                            parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(7)").attributes[
                                "title"][5:]
                    except:
                        series = "NA"
                    try:
                        model = parser.css_first("a.disabled").text()
                    except:
                        model = "NA"
                    try:
                        price = parser.css_first(
                            "div.body-wrapper > div.main > div.trim-main > h3 > span:nth-child(1) > font").text().strip()
                    except:
                        price = "NA"
                    data = [year, brand, series, model, price] + result
                    print(data)
                    try:
                        row = pd.Series(data,
                                        index=["年份", "品牌", "車系", "車型", "價格", "動力型式", "排氣量", "驅動型式", "輪胎尺碼", "車身型式", "車重"])
                    except ValueError:
                        with open("fail_extract_log.csv", "a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([url, result, data])
                        pass
                    else:
                        print(row)
                        self.df = self.df.append(row, ignore_index=True)
                    # print(url)
        return self.df

    def data_extract(self, all_cars=[]):
        # with open("test_file.csv", "w", newline="") as car_file:
        #     writer = csv.writer(car_file)
        #     writer.writerow(["Year", "Brand", "Category", "Model", "Exhaust volume", "Tire size"])
        #     last_session = HTMLSession()
        #     for mobile in all_cars:
        #         result = last_session.get(mobile, headers=self.random_header())
        #         try:
        #             result.html.xpath("//div[1]/div[1]/div[3]/div[4]/div[1]/ul[3]/li[4]/span[2]/text()")[0]
        #         except IndexError:
        #             tire_size = "NA"
        #         else:
        #             tire_size = result.html.xpath("//div[1]/div[1]/div[3]/div[4]/div[1]/ul[3]/li[4]/span[2]/text()")[0]
        #         try:
        #             result.html.xpath("//div[1]/div[1]/div[3]/div[4]/div[1]/ul[1]/li[3]/span[2]/text()")[0]
        #         except IndexError:
        #             exhaust = "NA"
        #         else:
        #             exhaust = result.html.xpath("//div[1]/div[1]/div[3]/div[4]/div[1]/ul[1]/li[3]/span[2]/text()")[0]
        #         try:
        #             result.html.xpath("//div[1]/div[1]/div[2]/span/a[3]/text()")[0]
        #         except IndexError:
        #             brand = "NA"
        #         else:
        #             brand = result.html.xpath("//div[1]/div[1]/div[2]/span/a[3]/text()")[0]
        #         try:
        #             result.html.xpath("//div[1]/div[1]/div[2]/span/a[4]/text()")[0]
        #         except IndexError:
        #             year = "NA"
        #             category = "NA"
        #         else:
        #             year_model = result.html.xpath("//div[1]/div[1]/div[2]/span/a[4]/text()")[0]
        #             year = year_model.split(" ")[0]
        #             category = " ".join(year_model.split(" ")[1:])
        #         try:
        #             result.html.xpath("//div[1]/div[1]/div[2]/span/a[5]/text()")[0]
        #         except IndexError:
        #             model = "NA"
        #         else:
        #             model = result.html.xpath("//div[1]/div[1]/div[2]/span/a[5]/text()")[0]
        #         writer.writerow([year, brand, category, model, exhaust, tire_size])
        #         sleep(randint(0, 1))
        #         print([year, brand, category, model, exhaust, tire_size])
        for car in all_cars:
            response = requests.get(car, headers=self.random_header())
            parser = HTMLParser(response.text)
            values = parser.css(
                "div.body-wrapper > div.main > div.trim-main > div.trim-spec-detail > div:nth-child(1) > ul > li > span:nth-child(2n)")
            keys = parser.css(
                "div.body-wrapper > div.main > div.trim-main > div.trim-spec-detail > div:nth-child(1) > ul > li > span:nth-child(2n-1)")
            target_info = ["動力型式", "排氣量", "驅動型式", "輪胎尺碼", "車身型式", "車重"]
            info_dict = dict()
            for key, value in zip(keys, values):
                print(key.text(), value.text())
                if key.text().strip() in target_info:
                    info_dict.setdefault(key.text().strip(), value.text().strip())
            result = list(info_dict.values())
            if "排氣量" not in info_dict.keys():
                result.insert(1, "NA")
            brand = parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(5)").text()
            year = parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(7)").text()[0:4]
            series = parser.css_first("div.body-wrapper > div.main > div.bread > span > a:nth-child(7)").text()[5:]
            model = parser.css_first("a.disabled").text()
            price = parser.css_first(
                "div.body-wrapper > div.main > div.trim-main > h3 > span:nth-child(1) > font").text().strip()
            data = [year, brand, series, model, price] + result
            row = pd.Series(data, index=["年份", "品牌", "車系", "車型", "價格", "動力型式", "排氣量", "驅動型式", "輪胎尺碼", "車身型式", "車重"])
            self.df = self.df.append(row, ignore_index=True)
        return self.df



crawler = YahooCarCrawler()
# brands = crawler.get_brands_sites()
# model = crawler.get_all_models(brands) #有車系清單的話就不用調用get_all_models()
model = pd.read_csv("all_model_links.csv", header=None)[0].values.tolist()
df = crawler.all_car_links(model)
df.to_excel("yahoo_car_oe_spec.xlsx", index=False)
print(df)

df["前輪尺寸"] = df["輪胎尺碼"].str.split(" ", expand=True)[0]
df["後輪尺寸"] = df["輪胎尺碼"].str.split(" ", expand=True)[1]
df = df[["年份", "品牌", "車系", "車型", "價格", "動力型式", "排氣量", "驅動型式", "車身型式", "車重", "前輪尺寸", "後輪尺寸"]]
df.to_excel("yahoo_car_oe_spec.xlsx", index=False)
