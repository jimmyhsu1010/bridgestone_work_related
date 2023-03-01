from playwright.sync_api import sync_playwright, Playwright, expect
from selectolax.parser import HTMLParser
import pandas as pd

url = "https://www.investing.com/commodities/brent-oil-historical-data"

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        # page.wait_for_load_state("networkidle")
        page.locator(".DatePickerWrapper_icon__Qw9f8").click()
        page.locator("div.NativeDateInput_root__wbgyP > input[value='2023-02-01']")
        # page.get_by_role("button", name="Apply").click()
        # df = pd.read_html(page.content())
        # print(df)
        
        # context.close()
        # page.close()
        
        
if __name__ == "__main__":
    run()
