# import pytest
# import toml
# from playwright.sync_api import Page, expect

# config = toml.load("conf.toml")
# xpaths = toml.load("xpath.toml")["xpaths"]
# url = config["app"]["url"]

# def verify_elements(page):
#     expect(page.locator(xpaths["bot_logo"])).to_be_visible()
#     expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
#     expect(page.locator(xpaths["top_heading_text"])).to_be_visible()

    # schedule_btn = page.locator(xpaths["schedule_appointment"])
    # expect(schedule_btn).to_be_visible()
    # schedule_btn.click()
