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
        3. Fill in the username and PIN fields.
        4. Click the login button.
        5. Wait for redirect back to Super 6 and confirm login.
        6. Maintain session for further actions.
        """
        self.start_browser()
        self.driver.get("https://super6.skysports.com/play")
        time.sleep(2)  # Wait for redirect and page load

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

    def take_screenshot(self, filename):
        if self.driver:
            self.driver.save_screenshot(filename)

    def close(self):
        if self.driver:
            self.driver.quit()

    # Additional methods for fetching fixtures, submitting picks, etc. will go here
