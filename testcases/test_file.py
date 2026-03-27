import pytest
import toml
from playwright.sync_api import Page, expect
 
@pytest.fixture(scope="session")
def bot_session(playwright):
    """
    Launches browser, navigates to the URL, and yields (page, xpaths).
    """
    config = toml.load("conf.toml")
    xpaths = toml.load("xpath.toml")["xpaths"]
    url = config["app"]["url"]
   
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
 
#@pytest.mark.smoke
def test_chatbot_is_visible(bot_session):
    """
    Test that the chatbot launcher is visible.
    """
    page, xpaths = bot_session
    chatbot_launcher = page.locator(xpaths["chatbot_launcher"])
   
    # Wait for the launcher and assert it is visible
    expect(chatbot_launcher).to_be_visible()
    print("Verified: Chatbot launcher is visible.")
 
#@pytest.mark.smoke
#@pytest.mark.regression
def test_chatbot_clickable(bot_session):
    """
    Test that the chatbot launcher opens the welcome screen and shows all expected elements.
    """
    page, xpaths = bot_session
   
    # 1. Click Launcher
    chatbot_launcher = page.locator(xpaths["chatbot_launcher"])
    chatbot_launcher.click()
   
    # 2. Wait for welcome screen and verify all its elements
    #page.wait_for_selector(xpaths["carousel_img"])
    expect(page.locator(xpaths["carousel_img"]).first).to_be_visible()
   
    # 3. Verify all 5 language options are visible
    expect(page.locator(xpaths["begin_english"])).to_be_visible()
    expect(page.locator(xpaths["begin_spanish"])).to_be_visible()
    expect(page.locator(xpaths["begin_french"])).to_be_visible()
    expect(page.locator(xpaths["begin_creole"])).to_be_visible()
    expect(page.locator(xpaths["begin_arabic"])).to_be_visible()
   
    # 4. Verify Terms & Conditions footer
    expect(page.locator(xpaths["terms_link"])).to_be_visible()
   
    print("Verified: Welcome screen, carousel image, language options, and footer are visible.")

    # 5. Verify the ticker in all 5 languages
    expect(page.locator(xpaths["ticker"])).to_be_enabled()

    print("Verified: ticker is visible in 5 langauges")

    # # 6. Verify  begin in spanish button is clickable
    # click_begin_spanish = page.locator(xpaths["begin_spanish"])
    # click_begin_spanish.click()
    # # verify conversation screen opens
    # expect(page.locator(xpaths["bot_logo"])).to_be_visible()
    # expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
    # expect(page.locator(xpaths["top_heading_text"])).to_be_visible()
    # # click on cross icon
    # config = toml.load("conf.toml")
    # expect_title = config["language"]["spanish"]
    # cross = f"//li[@title='{expect_title}']"
    # expect(page.locator(cross)).to_be_visible()
    # page.locator(cross).click() 

    # print("Verified: Top heading in spanish is visible")

    # # 7. Verify  begin in french button is clickable
    # chatbot_launcher.click()
    # click_begin_french = page.locator(xpaths["begin_french"])
    # click_begin_french.click()
    # # verify conversation screen opens
    # expect(page.locator(xpaths["bot_logo"])).to_be_visible()
    # expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
    # expect(page.locator(xpaths["top_heading_text"])).to_be_visible()
    # # click on cross icon
    # config = toml.load("conf.toml")
    # expect_title = config["language"]["french"]
    # cross = f"//li[@title='{expect_title}']"
    # expect(page.locator(cross)).to_be_visible()
    # page.locator(cross).click() 

    # # 8. Verify  begin in haitan cerole  button is clickable
    # chatbot_launcher.click()
    # click_begin_creole = page.locator(xpaths["begin_creole"])
    # click_begin_creole.click()
    # # verify conversation screen opens
    # expect(page.locator(xpaths["bot_logo"])).to_be_visible()
    # expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
    # expect(page.locator(xpaths["top_heading_text"])).to_be_visible()
    # # click on cross icon
    # config = toml.load("conf.toml")
    # expect_title = config["language"]["creole"]
    # cross = f"//li[@title='{expect_title}']"
    # expect(page.locator(cross)).to_be_visible()
    # page.locator(cross).click() 

    # # 9. Verify  begin in arabic  button is clickable
    # chatbot_launcher.click()
    # click_begin_arabic = page.locator(xpaths["begin_arabic"])
    # click_begin_arabic.click()
    # # verify conversation screen opens
    # expect(page.locator(xpaths["bot_logo"])).to_be_visible()
    # expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
    # expect(page.locator(xpaths["top_heading_text"])).to_be_visible()    
    # # click on cross icon
    # config = toml.load("conf.toml")
    # expect_title = config["language"]["arabic"]
    # cross = f"//li[@title='{expect_title}']"
    # expect(page.locator(cross)).to_be_visible()
    # page.locator(cross).click() 


    # 10. Verify  begin in english button is clickable
    # chatbot_launcher.click()
    click_begin_english = page.locator(xpaths["begin_english"])
    click_begin_english.click()
    # verify conversation screen opens
    expect(page.locator(xpaths["bot_logo"])).to_be_visible()
    expect(page.locator(xpaths["NIJC_assistant"])).to_be_visible()
    expect(page.locator(xpaths["top_heading_text"])).to_be_visible()

    #11.  Schedule or Change Appointment 
    text = "Schedule or Change Appointment"
    schedule_btn = page.locator(f"//span[normalize-space()='{text}']")
    expect(schedule_btn).to_be_visible()
    schedule_btn.click()
    print(f" Clicked option: {text}")

    # Verify user selection
    user_text = 'Schedule or Change Appointment'
    # expect(page.locator(f"//span[normalize-space()='{text}']")).to_have_text({user_text})
    expect(schedule_btn).to_have_text(text)
    print(f" User selection verified: '{text}'")

    # Verify chatbot response
    chatbot_text = 'What would you like to do?'
    expect(page.locator(xpaths["chatbot_response"])).to_be_visible()
    expect(page.locator(xpaths["chatbot_response"])).to_have_text(chatbot_text)

    #Verify the chatbot options
    config = toml.load("conf.toml")

    # Option 1
    text1 = config["schedule_apmnt"]["request_appointment"]
    option_1 = page.locator(f"//button[contains(@title,'{text1}')]")
    expect(option_1).to_be_visible()

    # Option 2
    text2 = config["schedule_apmnt"]["followup_appointment"]
    option_2 = page.locator(f"//button[contains(@title,'{text2}')]")
    expect(option_2).to_be_visible()

    # Option 3
    text3 = config["schedule_apmnt"]["reschedule_appointment"]
    option_3 = page.locator(f"//button[contains(@title,'{text3}')]")
    expect(option_3).to_be_visible()

    # Option 4
    text4 = config["schedule_apmnt"]["cancel_appointment"]
    option_4 = page.locator(f"//button[contains(@title,'{text4}')]")
    expect(option_4).to_be_visible()


    #12. select 'REquest a new appointment' from chatbot response
    option_1.click()

    # Verify user selection
    user_text = 'Request a New Appointment'
    expect(option_1).to_have_text(user_text)
    print(f" User selection verified: '{user_text}'")

     # Verify chatbot response
    chatbot_text = " I'm going to ask you some questions to determine you are eligible to schedule an appointment. This will take about 3-5 minutes. Would you like to proceed?"
    chatbot_response_last = page.locator(xpaths["chatbot_response"]).last
    expect(chatbot_response_last).to_be_visible()
    expect(chatbot_response_last).to_contain_text("I'm going to ask you some questions")


    #Verify the chatbot options
    config = toml.load("conf.toml")
    # Option 1
    text1 = config["select"]["Yes"]
    option_1 = page.locator(f"//button[contains(@title,'{text1}')]")
    expect(option_1).to_be_visible()
    # Option 2
    text2 = config["select"]["No"]
    option_2 = page.locator(f"//button[contains(@title,'{text2}')]")
    expect(option_2).to_be_visible()

    #13. select 'Yes' from chatbot response
    option_1.click()

    # Verify user selection
    user_text = 'Yes'
    expect(option_1).to_have_text(user_text)
    print(f" User selection verified: '{user_text}'")

    # Verify chatbot response
    chatbot_text = "What service do you need? Please select one of these options."
    chatbot_response_last = page.locator(xpaths["chatbot_response"]).last
    expect(chatbot_response_last).to_be_visible()
    expect(chatbot_response_last).to_contain_text("What service do you need? Please select one of these options.")

    #Verify the chatbot options
    config = toml.load("conf.toml")
    # Option 1
    text1 = config["services"]["Detention_Representation"]
    option_1 = page.locator(f"//button[contains(@title,'{text1}')]")
    expect(option_1).to_be_visible()
    # Option 2
    text2 = config["services"]["Asylum"]
    option_2 = page.locator(f"//button[contains(@title,'{text2}')]")
    expect(option_2).to_be_visible()

    # Option 3
    text3 = config["services"]["U_Visa"]
    option_3 = page.locator(f"//button[contains(@title,'{text3}')]")
    expect(option_3).to_be_visible()

    # Option 4
    text4 = config["services"]["DACA"]
    option_4 = page.locator(f"//button[contains(@title,'{text4}')]")
    expect(option_4).to_be_visible()

    # Option 5
    text5 = config["services"]["VAWA"]
    option_5 = page.locator(f"//button[contains(@title,'{text5}')]")
    expect(option_5).to_be_visible()

    # Option 6
    text6 = config["services"]["TPS"]
    option_6 = page.locator(f"//button[contains(@title,'{text6}')]")
    expect(option_6).to_be_visible()

    # Option 7
    text7 = config["services"]["Naturalization"]
    option_7 = page.locator(f"//button[contains(@title,'{text7}')]")
    expect(option_7).to_be_visible()

    # Option 8
    text8 = config["services"]["Family_Based_Immigration"]
    option_8 = page.locator(f"//button[contains(@title,'{text8}')]")
    expect(option_8).to_be_visible()

    # Option 9
    text9 = config["services"]["Other_Immigration_Assistance"]
    option_9 = page.locator(f"//button[contains(@title,'{text9}')]")
    expect(option_9).to_be_visible()

    #14. select 'Detention representation' from chatbot response
    option_1.click()
    # Verify user selection
    user_text = 'Detention Representation'
    expect(option_1).to_have_text(user_text)
    print(f" User selection verified: '{user_text}'")


    # Verify chatbot response
    chatbot_text = "Do you currently live in the United States?"
    chatbot_response_last = page.locator(xpaths["chatbot_response"]).last
    expect(chatbot_response_last).to_be_visible()
    expect(chatbot_response_last).to_contain_text("Do you currently live in the United States?")

    #Verify the chatbot options
    config = toml.load("conf.toml")
    # Option 1
    text1 = config["select"]["Yes"]
    option_1 = page.locator(f"//button[contains(@title,'{text1}')]").last
    expect(option_1).to_be_visible()
    # Option 2
    text2 = config["select"]["No"]
    option_2 = page.locator(f"//button[contains(@title,'{text2}')]").last
    expect(option_2).to_be_visible()

    #15. select 'Yes' from chatbot response
    option_1.click()

    # Verify user selection
    user_text = 'Yes'
    expect(option_1).to_have_text(user_text)
    print(f" User selection verified: '{user_text}'")

    # Verify chatbot response
    chatbot_text = "Please select the state where you currently live."
    chatbot_response_last = page.locator(xpaths["chatbot_response"]).last
    expect(chatbot_response_last).to_be_visible()
    expect(chatbot_response_last).to_contain_text("Please select the state where you currently live.")

    #Verify the chatbot options
    config = toml.load("conf.toml")
    # Option 1
    text1 = config["state"]["Illinios"]
    option_1 = page.locator(f"//button[contains(@title,'{text1}')]")
    expect(option_1).to_be_visible()
    # Option 2
    text2 = config["state"]["Indiana"]
    option_2 = page.locator(f"//button[contains(@title,'{text2}')]")
    expect(option_2).to_be_visible()
    # Option 3
    text3 = config["state"]["other"]
    option_3 = page.locator(f"//button[@title='{text3}']")
    expect(option_3).to_be_visible()

    #16. select 'Illinios' from chatbot response
    option_1.click()

    # Verify user selection
    user_text = 'Illinios'
    expect(option_1).to_have_text(user_text)
    print(f" User selection verified: '{user_text}'")













