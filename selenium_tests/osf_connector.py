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

    # 7) Click on settings icon
    try:
        settings_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/button[1]")
            )
        )
        settings_button.click()
        print("Clicked on settings icon!")
        
        # Wait a moment for the settings panel to open
        time.sleep(2)
        
    except Exception as e:
        print("Failed to find or click the settings icon:", str(e))

    # 8) Click on connect button
    try:
        # Store current window handle before clicking
        current_window = driver.current_window_handle
        print(f"Current window handle: {current_window}")
        
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div/div/div/div/div/div[3]/button/span[1]")
            )
        )
        connect_button.click()
        print("Clicked on connect button!")
        
        # Wait for new tab/window to open
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        
        # Get all window handles
        all_windows = driver.window_handles
        print(f"All window handles: {all_windows}")
        
        # Switch to the new tab (the one that's not the current window)
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
                print(f"Switched to new tab: {window}")
                break
        
        # Wait for the new page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print(f"New tab URL: {driver.current_url}")
        print("Successfully switched to the new tab!")
        
        # 9) Fill in login credentials on the new tab
        try:
            # Wait for username field to be present and fill it
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys(USERNAME)
            print("Filled username field!")
            
            # Wait for password field to be present and fill it
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.clear()
            password_field.send_keys(PASSWORD)
            print("Filled password field!")
            
            # Submit the form (you can either press Enter or find a submit button)
            # Option 1: Press Enter on password field
            password_field.send_keys(Keys.RETURN)
            print("Submitted login form!")
            
            # Option 2: If there's a specific login button, uncomment below:
            # login_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            # )
            # login_button.click()
            
            # Wait for successful login (adjust the condition based on what happens after login)
            time.sleep(3)  # Give some time for the login to process
            print(f"Login completed! Current URL: {driver.current_url}")
            
        except Exception as e:
            print("Failed to fill login credentials on new tab:", str(e))
        
    except Exception as e:
        print("Failed to find connect button or switch tabs:", str(e))

finally:
    # Close all windows
    driver.quit()
