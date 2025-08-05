from typing import Optional
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from . import config

logger = logging.getLogger(__name__)


class Super6Client:
    """
    Automates Super6 login and prediction submission.
    """

    def __init__(self) -> None:
        self.base_url: str = config.BASE_URL
        self.username: str = config.USERNAME
        self.pin: str = config.PIN
        self.driver: Optional[webdriver.Chrome] = None

    def start_browser(self, headless: bool = True) -> None:
        """
        Start a Chrome browser session with specified options.
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            logger.error("Failed to start Chrome WebDriver: %s", e)
            raise

    def login(self) -> None:
        """
        Log in to Super6 using Selenium automation.
        """
        self.start_browser()
        assert self.driver is not None, "WebDriver not initialized."

        self.driver.get(self.base_url)
        time.sleep(2)  # Wait for redirect and page load

        self._accept_cookies()

        try:
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.clear()
            username_input.send_keys(self.username)

            pin_input = self.driver.find_element(By.NAME, "password")
            pin_input.clear()
            pin_input.send_keys(self.pin)

            login_button = self.driver.find_element(By.ID, "login-submit")
            login_button.click()
        except NoSuchElementException as e:
            logger.error("Login form element not found: %s", e)
            self.take_screenshot('login_error.png')
            raise

        time.sleep(5)  # Wait for login to complete
        self.take_screenshot('login_result.png')

    def auto_pick_and_submit(self) -> Optional[str]:
        """
        Automate prediction selection and submission.

        Returns:
            'already_submitted' if predictions already submitted, otherwise None.
        """
        assert self.driver is not None, "WebDriver not initialized."

        self._accept_cookies()
        self.driver.get(self.base_url)
        time.sleep(2)

        if self._already_submitted():
            logger.info("Predictions already submitted.")
            self.take_screenshot('already_submitted.png')
            return 'already_submitted'

        self._set_predictions()
        self._set_golden_goal('10')
        self._submit_predictions()

        if self._already_submitted():
            logger.info("Predictions submitted successfully.")
        else:
            logger.warning("Submission may have failed. Please check submission_result.png.")

        self.take_screenshot('submission_result.png')
        return None

    def _accept_cookies(self) -> None:
        """
        Accept cookies if the banner is present.
        """
        try:
            accept_cookies = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_cookies.click()
            time.sleep(1)
        except NoSuchElementException:
            pass

    def _already_submitted(self) -> bool:
        """
        Check if predictions have already been submitted.
        """
        current_url = self.driver.current_url
        if "/played" in current_url:
            return True
        try:
            submitted_banner = self.driver.find_element(
                By.XPATH,
                '//div[contains(@class, "eqa0sqc1") and contains(., "Predictions Submitted")]'
            )
            return submitted_banner is not None
        except NoSuchElementException:
            return False

    def _set_predictions(self) -> None:
        """
        Set predictions for each match 1-0 for home team.
        """
        try:
            increase_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, 'button[data-test-id="match-team-prediction-home-increase"]'
            )
            for btn in increase_buttons:
                try:
                    btn.click()
                    time.sleep(0.2)
                except Exception as e:
                    logger.warning("Failed to click increase button: %s", e)
        except Exception as e:
            logger.error("Error setting predictions: %s", e)

    def _set_golden_goal(self, value: str) -> None:
        """
        Set the golden goal input value.
        """
        try:
            golden_goal_input = self.driver.find_element(
                By.CSS_SELECTOR, 'input[data-test-id="play-golden-goal-input"]'
            )
            golden_goal_input.clear()
            golden_goal_input.send_keys(value)
        except NoSuchElementException:
            logger.warning("Golden goal input not found.")

    def _submit_predictions(self) -> None:
        """
        Click the submit predictions button.
        """
        try:
            submit_btn = self.driver.find_element(
                By.CSS_SELECTOR, 'button[data-test-id="predictions-submit-button"]'
            )
            submit_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            logger.warning("Submit button not found.")

    def take_screenshot(self, filename: str) -> None:
        """
        Save a screenshot of the current browser window.
        """
        if self.driver:
            self.driver.save_screenshot(filename)

    def close(self) -> None:
        """
        Close the browser session.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None