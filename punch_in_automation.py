from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ehrportal.bridgestone.com.tw/ehrportal/loginFOrginal.asp")
    page.locator("select[name=\"companyid\"]").select_option("1")
    page.locator("input[name=\"username\"]").click()
    page.locator("input[name=\"username\"]").fill("111012")
    page.locator("input[name=\"password\"]").click()
    page.locator("input[name=\"password\"]").fill("111012")
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="登錄").click()
    page1 = page1_info.value
    page1.locator("div > a").click()
    page1.frame_locator("iframe[name=\"frmMAIN\"]").get_by_role("radio").first.check()
    page1.frame_locator("iframe[name=\"frmMAIN\"]").get_by_role("radio").nth(1).check()
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)