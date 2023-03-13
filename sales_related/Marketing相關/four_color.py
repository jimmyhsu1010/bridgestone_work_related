from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd

place_list = ["臺北市區監理所", "臺北區監理所", "宜蘭監理站", "花蓮監理站", "新竹區監理所", "新竹市監理站", "桃園監理站", "中壢監理站", "苗栗監理站", "臺中區監理所", "豐原監理站", "彰化監理站", "南投監理站", "雲林監理站", "嘉義市監理站", "麻豆監理站", "臺南監理站", "高雄市區監理所", "旗山監理站", "高雄區監理所", "屏東監理站", "臺東監理站"]
tour_bus_list = [
    "KAA-0", "KAA-1", "KAA-3", "KAA-5", "KAA-6", "KAA-7", "KAA-8", "KAA-9", "KAB-0", "KAB-1", "KAB-5", 
    "KAC-", "KAD-", "KAE-", "KAF-", "KAG-", "KAH-", "KAJ-", "KAL-", 
    "-V5", "-V6", "-V7", "-V8", "-V9", "-W2",
    "-AA", "-BB", "-CC", "-DD", "-FF", "-GG", "-HH", "-JJ", "-KK", "-LL",
    "A2-", "A3-", "A4-", "A5-", "Z5-", "Y3-", "9U-", "AA-", "BB-", "CC-", "DD-",
    "SS-", "TT-", "YY-", "-PP", "JYA-", "KQA-"
]


def get_car_info(fetch_list):
    dfs = []
    if "新竹區監理所" in fetch_list:
        url = "https://leak.gewohler.icu/hpvdb.php?strs=%20"
    else:
        url = "https://leak.gewohler.icu/hpvdb-tour.php?strs=%20"
    for code in fetch_list:
        new_url = url + code
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(new_url, wait_until="networkidle", timeout=0)
            page.wait_for_load_state("networkidle")
            try:
                taipei_truck = pd.read_html(page.content())
            except ValueError:
                print(new_url)
                pass
            else:
                df = pd.DataFrame(taipei_truck[0])
                # print(df)
                dfs.append(df)
                page.close()
            
    result = pd.concat(dfs)
    result = result.drop_duplicates()
    if "新竹區監理所" in fetch_list:
        result.to_excel(r"D:\kc.hsu\OneDrive - Bridgestone\數據\市場資訊\大車監理數據.xlsx", index=False) 
    else:
        result.to_excel(r"D:\kc.hsu\OneDrive - Bridgestone\數據\市場資訊\遊覽車業者.xlsx", index=False) 
    

if __name__ == "__main__":
    select_dict = {1: place_list, 2: tour_bus_list}
    for key, value in select_dict.items():
        print(key, value)
    answer = eval(input("Please select the data you want to fetch. \n"))
    get_car_info(select_dict[answer])
    
