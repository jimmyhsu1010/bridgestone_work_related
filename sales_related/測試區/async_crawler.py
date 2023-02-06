from requests_html import AsyncHTMLSession, HTMLSession
import asyncio
from time import sleep
from random import randint
import csv
from datetime import datetime

def random_agent():
    with open("user_agent.text") as f:
        user_agent_list = [line.rstrip("\n") for line in f]
        return user_agent_list



def random_header(usr_agent=[]):
    random_agent = usr_agent[randint(0, len(usr_agent) - 1)]
    headers = {"User-Agent": random_agent, }
    return headers


def get_car_brands():
    start_page = "https://autos.yahoo.com.tw/new-cars/research/"
    session = HTMLSession()
    response = session.get(start_page)
    brands = response.html.find("div.research-main > div.research-wrapper > div.list > a.gabtn")
    brand_links = [i.attrs["href"] for i in brands]
    return brand_links


async def get_all_models(s, link):
    user_agent_list = random_agent()
    response = await s.get(link, headers=random_header(user_agent_list))
    models = []
    # render裡面需要有parameters，sleep讓他有時間可以讀取，scrolldown模擬滑鼠要往下拉多少
    response.html.arender()
    for r in response.html.find("div.make-main.jq-make-wrapper > div"):
        if "data-year" in r.attrs.keys():
            # print(j.attrs["data-year"])
            for model in r.find("a.gabtn"):
                models.append(model.attrs["href"])
                print(model.attrs["href"])
    sleep(randint(0, 1))
    # print(len(models))
    return models


car_brands = get_car_brands()
# user_agent_list = random_agent()

async def main(urls):
    s = AsyncHTMLSession()
    tasks = (get_all_models(s, url) for url in urls)
    return await asyncio.gather(*tasks)

result = asyncio.run(main(car_brands))


# s = AsyncHTMLSession()
# res = s.get('https://autos.yahoo.com.tw/new-cars/make/ford', headers=random_header(user_agent_list))
# await res.html.arender(sleep=1, keep_page=True, scrolldown=10)






