import time
import os
from dotenv import load_dotenv
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
load_dotenv()
USERNAME    = os.getenv("RDS_USER")
PASSWORD    = os.getenv("RDS_PASS")
LOGIN_URL   = "https://rds-ng-internal.uni-muenster.de/login?clear=1"


# Set up headless Firefox
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    # 1) Go to the login page
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "user"))
    )

    # 2) Fill in credentials and submit
    driver.find_element(By.NAME, "user").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)

    # 3) Wait until redirected to dashboard or home
    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.url_contains("dashboard"),
            EC.url_contains("home")
        )
    )
    print("Login successful, on dashboard.")

    # 4) Wait for the menu to render
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.app-menu-main"))
    )

    # 5) Locate and click the "BridgIT" item under data-app-id="rdsng"
    try:
        bridgit_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "li[data-app-id='rdsng'] > a")
            )
        )
        # Scroll it into view then click
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            bridgit_link
        )
        bridgit_link.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains("/apps/rdsng/main")
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.app-main-content"))
        )
        print("Clicked on BridgIT menu entry!")
    except Exception as e:
        print("Failed to find or click the BridgIT menu item:", str(e))

    # 6) Switch into the iframe
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "app-frame"))
    )
    print("Switched into app-frame iframe!")
    # 7) Click the settings icon
    settings_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[contains(@class,'mi-settings')]]"
        ))
    )
    settings_btn.click()
    print("Clicked settings icon.")

    # 8) Click "Add a new connection..." placeholder
    add_conn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "span.p-select-label.p-placeholder[aria-label='Add a new connection...']"
        ))
    )
    add_conn.click()
    print("Opened new connection dropdown.")

    # 9) Wait for the dropdown list to expand (uses the aria-controls ID)
    options_container = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "pv_id_1_10_list"))
    )

    # 10) Click the second option in the list
    second_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#pv_id_1_10_list li[role='option']:nth-child(2)"
        ))
    )
    second_option.click()
    print("Selected second connection option.")
    #time.sleep(10)
    # 11) Fill in the connection “Name” field
    conn_name = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "name"))
    )
    conn_name.clear()
    conn_name.send_keys("My Connection Name")
    print("Filled connection name.")

    # 12) Fill in the connection “Description” textarea
    conn_desc = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "description"))
    )
    conn_desc.clear()
    conn_desc.send_keys("This is a description for my new connection.")
    print("Filled connection description.")

    # 13) Click the “Create” button
    create_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[text()='Create']]"
        ))
    )
    create_btn.click()
    print("Clicked Create button for new connection!")

    
finally:
    driver.quit()
