import time
import os
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
load_dotenv()
USERNAME    = os.getenv("RDS_USER")
PASSWORD    = os.getenv("RDS_PASS")
LOGIN_URL   = os.getenv("RDS_URL")



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

    # 7) Click the "New project" button
    new_proj_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="New project"]'))
    )
    new_proj_btn.click()
    time.sleep(2)  # brief pause for the dialog to appear

    # 8) Wait for the Name field and fill it
    name_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "title"))
    )
    name_input.clear()
    name_input.send_keys("My Awesome Project")
    print("Filled in project name.")

    # 9) Wait for the Description textarea and fill it
    desc_area = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "description"))
    )
    desc_area.clear()
    desc_area.send_keys("This is a description for my awesome project.")
    print("Filled in project description.")
    # 10) Wait for the "Next" button and click it
    next_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
        By.XPATH,
        "//button[.//span[text()='Next']]"
        ))
      )
    next_btn.click()
    # 11) Select the “All files” tree node
    all_files_node = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'p-tree-node-content') and .//span[text()='All files']]"
        ))
    )
    all_files_node.click()
    print("Selected 'All files' node.")

    # 12) Click the Next button again
    next_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[text()='Next']]"
        ))
    )
    next_btn.click()
    print("Clicked Next button!")
    


    # 13) Click the first (large) checkbox with ActionChains
    first_checkbox = WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.p-checkbox-box[data-p='large']"))
    )
    ActionChains(driver).move_to_element(first_checkbox).click().perform()
    print("Clicked first checkbox with ActionChains.")

    # 14) Click the second (dmp) checkbox with ActionChains
    second_checkbox = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#dmp"))
    )
    ActionChains(driver).move_to_element(second_checkbox).click().perform()
    print("Clicked 'dmp' checkbox with ActionChains.")

    # 15) Click the arrow‐forward “Next” button
    next_arrow = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[contains(@class,'mi-arrow-forward')]]"
        ))
    )
    next_arrow.click()
    print("Clicked the next arrow button.")
    # 16) Click the "Create" button
    create_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[.//span[text()='Create']]"
        ))
    )
    create_btn.click()
    print("Clicked Create button!")
    time.sleep(10)

finally:
    driver.quit()

