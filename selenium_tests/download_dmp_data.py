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
USERNAME  = os.getenv("RDS_USER")
PASSWORD  = os.getenv("RDS_PASS")
LOGIN_URL = os.getenv("RDS_URL")

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
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "app-frame"))
    )

    # 7) Click the “My Awesome Project” card itself using a CSS selector
    project_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".projects-listbox-container div[title='My Awesome Project']"
        ))
    )
    project_card.click()
    print("Clicked on 'My Awesome Project'.")

    # 8) Click the “Data Management Plan” tab by its visible label
    dmp_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[text()='Data Management Plan']]"
        ))
    )
    dmp_tab.click()
    print("Clicked the Data Management Plan tab.")

    # 9) Click the “PDF” export button
    pdf_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="PDF"]'))
    )
    pdf_btn.click()
    print("Clicked PDF export button.")

    # 10) Click the “Plain Text” export button
    text_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Plain Text"]'))
    )
    text_btn.click()
    print("Clicked Plain Text export button.")

finally:
    driver.quit()
