from playwright.sync_api import sync_playwright, Playwright, expect
from selectolax.parser import HTMLParser
import pandas as pd
from investiny import historical_data

url = "https://www.investing.com/commodities/brent-oil-historical-data"

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        data = pd.read_html(page.content())
        df = pd.DataFrame(data[1])
        print(df)
        
        context.close()
        page.close()
    return df
        
        
if __name__ == "__main__":
    update_df = run()
    db = pd.read_csv("sales_related/Marketing相關/Brent Oil Futures Historical Data.csv")
    result = pd.concat([update_df, db])
    result.drop_duplicates(subset="Date", keep="first", inplace=True)
    result.to_csv("sales_related/Marketing相關/Brent Oil Futures Historical Data.csv", index=False)
    