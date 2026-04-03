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

def test_login_form_is_visible(login):
    """
    Test that Login form opens and fields are visible 
    """
    page, xpaths = login   

    login_form = page.locator(xpaths["login_form"])  

    expect(login_form).to_be_visible()
    expect(page.locator(xpaths["nijc_logo"])).to_be_visible()
    login_topheading_1 = page.locator(xpaths["login_topheading"]).first
    expect(login_topheading_1).to_be_visible()
    # expect(login_topheading_1).inner()       

    print("Verified: Login form and logo is visible.")
     # Enter Email
    email_input = page.locator(xpaths["email_input"])
    expect(email_input).to_be_visible()
    email_input.fill("tanishauat@yopmail.com")

    # Enter Password
    password_input = page.locator(xpaths["password_input"])
    expect(password_input).to_be_visible()
    password_input.fill("Test@122")

    # Toggle password visibility (optional)
    toggle_btn = page.locator(xpaths["toggle_password"])
    toggle_btn.click()
    toggle_btn.click()

    # Click Login
    login_btn = page.locator(xpaths["login_button"])
    expect(login_btn).to_be_visible()
    login_btn.click()
    page.wait_for_timeout(100000)

    # Verify user landed on dashboard / homepage
    user_name = page.locator(xpaths["user_name"]).first
    if "/home" in page.url and page.locator(xpaths["user_name"]).is_visible():    
        print("Already on User Dashboard.")    
    expect(user_name).to_be_visible()

def test_profile_navigation(login):
    """
    Verify user can navigate to profile
    """
    page, xpaths = login

    profile_btn = page.locator(xpaths["profile_button"])
    expect(profile_btn).to_be_visible()
    profile_btn.click()


    profile_btn = page.locator(xpaths["profile_button"])
    expect(profile_btn).to_be_visible()
    profile_btn.click()

    profile_name = page.locator(xpaths["profile_name"]).nth(3)
    expect(profile_name).to_be_visible()
    profile_name.click()

    profile_email = page.locator(xpaths["profile_email"]).nth(2)
    expect(profile_email).to_be_visible()
    profile_email.click()

    profile_menu = page.locator(xpaths["profile_menu"])
    expect(profile_menu).to_be_visible()
    profile_menu.click()

    print("Profile opened")

    # ------------------ LANGUAGE ------------------
    language_dropdown = page.locator(xpaths["language_dropdown"])
    expect(language_dropdown).to_be_visible()
    language_dropdown.click()

    language_option = page.locator(xpaths["language_option"])
    expect(language_option).to_be_visible()
    language_option.click()

    # ------------------ NAME ------------------
    first_name = page.locator(xpaths["first_name"])
    expect(first_name).to_be_visible()
    first_name.fill("Tanisha")
    expect(first_name).to_have_value("Tanisha")

    middle_name = page.locator(xpaths["middle_name"])
    expect(middle_name).to_be_visible()
    middle_name.fill("New")
    expect(middle_name).to_have_value("New")

    last_name = page.locator(xpaths["last_name"])
    expect(last_name).to_be_visible()
    last_name.fill("User")
    expect(last_name).to_have_value("User")

    print("Name fields updated")

    # ------------------ DOB ------------------
    dob = page.locator(xpaths["dob"])
    expect(dob).to_be_visible()
    dob.click()

    page.locator(xpaths["month"]).click()
    page.locator(xpaths["year"]).click()
    page.locator(xpaths["day"]).click()

    # ------------------ GENDER ------------------
    gender = page.locator(xpaths["gender_dropdown"])
    expect(gender).to_be_visible()
    gender.click()

    page.locator(xpaths["gender_option"]).click()

    # ------------------ ADDRESS ------------------
    street = page.locator(xpaths["street"])
    expect(street).to_be_visible()
    street.fill("Main street 125N.")
    expect(street).to_have_value("Main street 125N.")

    apt = page.locator(xpaths["apt"])
    expect(apt).to_be_visible()
    apt.fill("Apt. 9B CGh")

    # ------------------ STATE ------------------
    state = page.locator(xpaths["state"])
    expect(state).to_be_visible()
    state.click()
    state.fill("illinios")

    state_option = page.locator(xpaths["state_option"])
    expect(state_option).to_be_visible()
    state_option.click()

    # ------------------ CITY ------------------
    city = page.locator(xpaths["city"]).first
    expect(city).to_be_visible()
    city.click()

    city_option = page.locator(xpaths["city_option"])
    expect(city_option).to_be_visible()
    city_option.click()

    # ------------------ ZIP ------------------
    zip_code = page.locator(xpaths["zip"])
    expect(zip_code).to_be_visible()
    zip_code.fill("67901")
    expect(zip_code).to_have_value("67901")

    # ------------------ EMAIL & PHONE ------------------
    email = page.locator(xpaths["email"])
    expect(email).to_be_visible()
    email.click()

    phone = page.locator(xpaths["phone"])
    expect(phone).to_be_visible()
    phone.click()

    # ------------------ CANCEL ------------------
    save_profile_btn = page.locator(xpaths["save_profile_btn"])
    expect(save_profile_btn).to_be_visible()
    save_profile_btn.click()

    print("Profile form saved successfully")










