import pytest
import toml
from playwright.sync_api import Page, expect
 
@pytest.fixture(scope="session")
def login(playwright):
    """
    Launches browser, navigates to the URL, and yields (page, userportal).
    """
    config = toml.load("conf.toml")
    xpaths = toml.load("xpath.toml")["userportal"]
    url = config["user"]["url"]
   
    # Launch browser
    browser = playwright.chromium.launch(
        headless=config["playwright"].get("headless", True)
    )
   
    # Create context and page
    context = browser.new_context(
    viewport=config["playwright"].get("viewport", {"width": 1280, "height": 720})
    )
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
   
    yield page, xpaths 
   
    # Cleanup
    browser.close()

def login_form_is_visible(login):
    page, xpaths = login   

    login_form = page.locator(xpaths["login_form"])   

    expect(login_form).to_be_visible()
    expect(page.locator(xpaths["nijc_logo"])).to_be_visible()

    print("Verified: Login form and logo is visible.")





 