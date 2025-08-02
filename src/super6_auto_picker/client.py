import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from src.super6_auto_picker import config

class Super6Client:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.username = config.USERNAME
        self.pin = config.PIN
        self.driver = None

    def start_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run headless for automation
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        """
        Perform login to Super 6 via SkyBet authentication using Selenium.
        Steps:
        1. Open Chrome and navigate to the Super 6 play URL.
        2. Wait for redirect to the SkyBet login page.
        3. Accept cookies if prompted.
        4. Fill in the username and PIN fields.
        5. Click the login button.
        6. Wait for redirect back to Super 6 and confirm login.
        7. Maintain session for further actions.
        """
        self.start_browser()
        self.driver.get("https://super6.skysports.com/play")
        time.sleep(2)  # Wait for redirect and page load

        # Accept cookies if the banner is present
        try:
            accept_cookies = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_cookies.click()
            time.sleep(1)  # Wait for the banner to disappear
        except Exception:
            pass  # If not present, continue

        # Fill in username
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys(self.username)

        # Fill in PIN (field is named 'password')
        pin_input = self.driver.find_element(By.NAME, "password")
        pin_input.clear()
        pin_input.send_keys(self.pin)

        # Click the login button
        login_button = self.driver.find_element(By.ID, "login-submit")
        login_button.click()

        # Wait for redirect and login to complete
        time.sleep(5)  # Adjust as needed for page load
        # Take a screenshot after login attempt
        self.take_screenshot('login_result.png')
        # TODO: Add logic to confirm successful login (e.g., check URL or page content)
        # TODO: Handle login errors and log them

    def auto_pick_and_submit(self):
        """
        After login, automate the following:
        1. Accept cookies again if prompted on super6.skysports.com
        2. Navigate to /play
        3. For each match, increase the home team score by one (set to 1-0)
        4. Enter '10' into the golden goal input
        5. Click the 'SUBMIT PREDICTIONS' button
        6. Take a screenshot after submission
        """
        import time
        from selenium.webdriver.common.by import By
        # Accept cookies again if present
        try:
            accept_cookies = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_cookies.click()
            time.sleep(1)
        except Exception:
            pass
        # Navigate to /play (in case not already there)
        self.driver.get("https://super6.skysports.com/play")
        time.sleep(2)
        # For each match, increase home team score by one
        increase_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-test-id="match-team-prediction-home-increase"]')
        for btn in increase_buttons:
            try:
                btn.click()
                time.sleep(0.2)
            except Exception:
                pass
        # Enter '10' into the golden goal input
        try:
            golden_goal_input = self.driver.find_element(By.CSS_SELECTOR, 'input[data-test-id="play-golden-goal-input"]')
            golden_goal_input.clear()
            golden_goal_input.send_keys('10')
        except Exception:
            pass
        # Click the submit predictions button
        try:
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="predictions-submit-button"]')
            submit_btn.click()
            time.sleep(2)
        except Exception:
            pass
        # Take a screenshot after submission
        self.take_screenshot('submission_result.png')

    def take_screenshot(self, filename):
        if self.driver:
            self.driver.save_screenshot(filename)

    def close(self):
        if self.driver:
            self.driver.quit()

    # Additional methods for fetching fixtures, submitting picks, etc. will go here
