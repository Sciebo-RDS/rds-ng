import time
import os
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from dotenv import load_dotenv

load_dotenv()
USERNAME    = os.getenv("RDS_USER")
PASSWORD    = os.getenv("RDS_PASS")
LOGIN_URL   = os.getenv("RDS_URL")

# Set up headless Firefox
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

wait = WebDriverWait(driver, 20)

def switch_to_default():
    try:
        driver.switch_to.default_content()
    except Exception:
        pass

def find_in_any_frame(by, sel, timeout_each=6):
    """
    Try to find element in default content; if not found, try each iframe (one level).
    Returns the element and leaves Selenium focused in the correct context.
    """
    switch_to_default()
    try:
        return WebDriverWait(driver, timeout_each).until(
            EC.presence_of_element_located((by, sel))
        )
    except TimeoutException:
        pass

    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for f in frames:
        try:
            driver.switch_to.frame(f)
            el = WebDriverWait(driver, timeout_each).until(
                EC.presence_of_element_located((by, sel))
            )
            return el
        except TimeoutException:
            switch_to_default()
            continue
        except StaleElementReferenceException:
            switch_to_default()
            continue

    switch_to_default()
    raise TimeoutException(f"Element not found: {by}={sel}")

try:
    # 1) Go to the login page
    driver.get(LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.NAME, "user")))

    # 2) Fill in credentials and submit
    driver.find_element(By.NAME, "user").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)

    time.sleep(2)
    print("Opened BridgIT page directly.")

    # 3) Switch into app iframe if present (#app-frame)
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "app-frame"))
        )
        print("Switched into app-frame iframe!")
    except TimeoutException:
        switch_to_default()
        print("app-frame not present yet; staying in default content.")

    # 4) Click "Authorize bridgit"
    try:
        authorize_label_xpath = "//span[contains(@class,'p-button-label') and normalize-space()='Authorize bridgit']"
        try:
            authorize_span = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, authorize_label_xpath))
            )
        except TimeoutException:
            switch_to_default()
            authorize_span = WebDriverWait(driver, 1).until(
                lambda d: find_in_any_frame(By.XPATH, authorize_label_xpath)
            )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", authorize_span)
        try:
            authorize_span.click()
        except Exception:
            parent_btn = authorize_span.find_element(By.XPATH, "./ancestor::button[1]")
            parent_btn.click()

        print("Clicked 'Authorize bridgit' button successfully!")
    except TimeoutException:
        print("Authorize bridgit button not found or not clickable (maybe already authorized).")

    # 5) Click "Anmelden"
    switch_to_default()
    try:
        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Anmelden']")),
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
        )

        anmelden_input = find_in_any_frame(By.CSS_SELECTOR, "input[type='submit'][value='Anmelden']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", anmelden_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Anmelden']")))
        anmelden_input.click()
        print("Clicked 'Anmelden' submit button.")
    except TimeoutException:
        print("Could not find the 'Anmelden' button after redirect.")

    # 6) Click "Zugriff gewähren"
    switch_to_default()
    try:
        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Zugriff gewähren']")),
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
        )

        zugriff_input = find_in_any_frame(By.CSS_SELECTOR, "input[type='submit'][value='Zugriff gewähren']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", zugriff_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Zugriff gewähren']")))
        zugriff_input.click()
        print("Clicked 'Zugriff gewähren' submit button.")
    except TimeoutException:
        print("Could not find the 'Zugriff gewähren' button after redirect.")
    time.sleep(10)    

finally:
    driver.quit()
