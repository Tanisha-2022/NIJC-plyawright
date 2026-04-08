import pytest
import toml
import re
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
    viewport=config["playwright"].get("viewport", {"width": 1480, "height": 920})
    )
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
   
    yield page, xpaths 
   
    # Cleanup
    browser.close()

# @pytest.mark.skip
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
    # Verify user landed on dashboard / homepage
    expect(page).to_have_url(re.compile(r".*/home"))
    print("Login successful")

# @pytest.mark.skip
def test_dashboard_loaded(login):
    """ Navigate to User Dashboard """
    page, xpaths = login
    # test_login_form_is_visible(login)
    page.wait_for_timeout(30000)
    welcome_text = page.locator(xpaths["welcome_text"])
    expect(welcome_text).to_be_visible()
    user_name = page.locator(xpaths["user_name"]).first      
    expect(user_name).to_be_visible()
    print("Already on User Dashboard.")

# @pytest.mark.skip
def test_profile_navigation(login):
    """
    Verify user can navigate to profile
    """
    page, xpaths = login
    profile_btn = page.locator(xpaths["profile_button"])
    expect(profile_btn).to_be_visible()
    profile_btn.click()
    profile_name = page.locator(xpaths["profile_name"])
    profile_email = page.locator(xpaths["profile_email"])
    expect(profile_email).to_be_visible()
    profile_menu = page.locator(xpaths["profile_menu"])
    expect(profile_menu).to_be_visible()
    profile_menu.click()
    # page.wait_for_timeout(15000)
    expect(page).to_have_url(re.compile(r".*/profile"))
    print("Profile opened")

# @pytest.mark.skip
def test_update_basic_profile(login):
    """ Enter the basic User Information"""
    page, xpaths = login

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

    # page.locator(xpaths["month"]).click()
    # page.locator(xpaths["year"]).click()
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
    # state.fill("Illinios")

    state_option = page.locator(xpaths["state_option"])
    expect(state_option).to_be_visible()
    state_option.click()

    # ------------------ CITY ------------------
    city = page.locator(xpaths["city"])
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
    print("Email has been verified")

    phone = page.locator(xpaths["phone"])
    expect(phone).to_be_visible()
    phone.click()
    print("Phone number has been verified")

# @pytest.mark.skip
def test_save_profile(login):
    """ Save the Primary User Profile """
    page, xpaths = login

    # ------------------ Save ------------------
    save_profile_btn = page.locator(xpaths["save_profile_btn"])
    expect(save_profile_btn).to_be_visible()
    save_profile_btn.click()
    expect(page.locator(xpaths["saved_taost"])).to_be_visible()
    print("Profile form saved successfully")

# @pytest.mark.skip
def test_household_details(login):
    """ Verify the household details of primary user"""
    page, xpaths = login
    expect(page.locator(xpaths["household_tab"])).to_be_visible()
    expect(page.locator(xpaths["household_text"])).to_be_visible()

    #---------spouse--------------------
    expect(page.locator(xpaths["partner_question"])).to_be_visible()
    partner_answer = page.locator(xpaths["partner_question"])
    expect(partner_answer).to_be_visible()
    partner_answer.click()

    #--------------children-----------------
    expect(page.locator(xpaths["children_question"])).to_be_visible()
    children_answer = page.locator(xpaths["children_answer"])
    expect(children_answer).to_be_visible()
    children_answer.click()
    expect(page.locator(xpaths["children_count"])).to_be_visible()
    page.locator(xpaths["children_count"]).click()

    #------------adult----------------
    expect(page.locator(xpaths["adult-question"])).to_be_visible()
    adult_count = page.locator(xpaths["adult_count"])
    expect(adult_count).to_be_visible()
    adult_count.click()

    #-------income-----------
    expect(page.locator(xpaths["income-question"])).to_be_visible()
    income_annswer = page.locator(xpaths["income_annswer"])
    expect(income_annswer).to_be_visible()
    income_annswer.click()

    save_profile_btn = page.locator(xpaths["save_profile_btn"])
    expect(save_profile_btn).to_be_visible()
    save_profile_btn.click()
    expect(page.locator(xpaths["saved_taost"])).to_be_visible()
    print("Household details saved successfully")

# @pytest.mark.skip
def test_dashboard_loaded_after_profile_setup(login):
    """ Navigate to User Dashboard after profile setup"""
    page, xpaths = login
    expect(page).to_have_url(re.compile(r".*/home"), timeout=15000)
    # NOW check dashboard element
    user_name = page.locator(xpaths["user_name"]).first
    expect(user_name).to_be_visible(timeout=15000) 
    # page.wait_for_timeout(50000)
    welcome_text = page.locator(xpaths["welcome_text"])
    expect(welcome_text).to_be_visible()
    user_name = page.locator(xpaths["user_name"]).first      
    expect(user_name).to_be_visible()
    expect(page.locator(xpaths["new_Appointment_btn"])).to_be_visible()
    expect(page.locator(xpaths["notification_icon"])).to_be_visible()
    expect(page.locator(xpaths["household_card"])).to_be_visible()
    expect(page.locator(xpaths["appointment_Section"])).to_be_visible()
    expect(page.locator(xpaths["view_all"])).to_be_visible()
    print("Already on User Dashboard.")

# @pytest.mark.skip
def test_my_appointment(login):
    """ Navigate to My appointment page and verify users"""
    page, xpaths = login

    page.locator(xpaths["view_all"]).click()
    expect(page).to_have_url(re.compile(r".*/my-appointments"), timeout=15000)
    expect(page.locator(xpaths["myappointment_heading_line"])).to_be_visible()
    expect(page.locator(xpaths["new_Appointment_btn"])).to_be_visible()
    print("My appointments page verification")
    # partner_answer.click()
    # page.locator(xpaths["partner_question"]).to_be_visible()
    # page.locator(xpaths["partner_question"]).to_be_visible()
    

    # page.locator(xpaths["saved_taost"]).to_be_visible()
