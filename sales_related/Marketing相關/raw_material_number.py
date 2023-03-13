from playwright.sync_api import sync_playwright, Playwright, expect
from selectolax.parser import HTMLParser
import pandas as pd


urls = ["https://www.investing.com/commodities/brent-oil-historical-data", "https://www.investing.com/commodities/rubber-rss3-futures-historical-data",
       "https://www.investing.com/commodities/rubber-tsr20-futures-historical-data", "https://www.investing.com/commodities/iron-ore-62-cfr-futures-historical-data?cid=992748", 
       "https://www.investing.com/commodities/coking-coal-futures-historical-data", "https://www.investing.com/commodities/rotterdam-coal-futures-historical-data"]

dbs = ["sales_related/Marketing相關/raw_material_price/Brent Oil Futures Historical Data.csv",
       "sales_related/Marketing相關/raw_material_price/Rubber RSS3 Futures Historical Data.csv",
       "sales_related/Marketing相關/raw_material_price/Rubber TSR20 Futures Historical Data.csv",
       "sales_related/Marketing相關/raw_material_price/Iron ore fines 62% Fe CFR Futures Historical Data.csv",
       "sales_related/Marketing相關/raw_material_price/Coking Coal Futures Historical Data.csv",
       "sales_related/Marketing相關/raw_material_price/Rotterdam Coal Futures Historical Data.csv"]

commoditys = ["Brent Oil", "Rubber RSS3", "Rubber TSR20", "Iron Ore Fines 62%", "Coking Coal", "Rotterdam Coal"]

scraping_dict = dict(zip(urls, zip(dbs, commoditys)))


def run():
    with sync_playwright() as pw:
        for url, infos in scraping_dict.items():
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            data = pd.read_html(page.content())
            df = pd.DataFrame(data[1])
            print(df)
            
            db = pd.read_csv(infos[0])
            result = pd.concat([df, db])
            result.drop_duplicates(subset="Date", keep="first", inplace=True)
            result["Type"] = infos[1]
            result.to_csv(infos[0], index=False)
            
            context.close()
            page.close()
        
        
if __name__ == "__main__":
    run()
    dfs = [pd.read_csv(path) for path in dbs]
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv("sales_related/Marketing相關/raw_material_price/raw_material_daily_price.csv", index=False)
    
    