from typing import Optional
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .utils.file_utils import read_predictions
from . import config

logger = logging.getLogger(__name__)

# Mapping of webpage team names to standardized names
TEAM_NAME_MAP = {
    "brighton": "Brighton and Hove Albion",
    "man utd": "Manchester United",
    "sunderland": "Sunderland",
    "west ham": "West Ham United",
    "spurs": "Tottenham Hotspur",
    "burnley": "Burnley",
    "wolves": "Wolverhampton Wanderers",
    "man city": "Manchester City",
    "chelsea": "Chelsea",
    "crystal palace": "Crystal Palace",
    "arsenal": "Arsenal",
    "fulham": "Fulham",
    "liverpool": "Liverpool",
    "newcastle": "Newcastle United",
    "nottm forest": "Nottingham Forest",
    "brentford": "Brentford",
    "bournemouth": "Bournemouth",
    "aston villa": "Aston Villa",
    "leeds": "Leeds United"
}


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

            # Try primary login button, fall back to alternative if not present
            try:
                login_button = self.driver.find_element(By.ID, "login-submit")
            except NoSuchElementException:
                logger.info("Primary login button 'login-submit' not found; trying fallback 'login'.")
                login_button = self.driver.find_element(By.ID, "login")

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

    def navigate_to_edit_mode(self) -> None:
        """
        Navigate to the edit mode by clicking the Edit button.
        """
        assert self.driver is not None, "WebDriver not initialized."

        try:
            edit_button = self.driver.find_element(By.ID, "js-fixtures-edit-entry")
            edit_button.click()
            time.sleep(2)  # Wait for the edit page to load
        except NoSuchElementException as e:
            logger.error("Edit button not found: %s", e)
            self.take_screenshot('edit_error.png')
            raise

    def intelligent_pick_and_submit(self) -> None:
        """
        Perform intelligent prediction setting by clicking edit and mapping teams to predictions.
        """
        self._accept_cookies()
        logger.info("Accepting cookies")

        if not self._already_submitted():
            try:
                # Click the "Play For Free" button
                play_for_free_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@data-target-id='s6-default-cta-play-btn' and text()='Play For Free']"))
                )
                play_for_free_button.click()
                time.sleep(2) 
                logger.info("Clicked Play For Free button")
                self.take_screenshot("clicked_play_for_free.png")
            except (NoSuchElementException, TimeoutException):
                raise Exception("Play For Free button not found, cannot proceed.")
        
        else:

            # Click the View Predictions link
            logger.info("Clicking View Predictions link")
            try:
                view_predictions_link = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/played') and text()='View Predictions']"))
                )
                view_predictions_link.click()
                logger.info("Clicked View Predictions link")
                self.take_screenshot("clicked_predicton_view.png")
                time.sleep(2)  # Wait for the page to load
                self.take_screenshot("view_predictions_page_after_sleep.png")
            except (NoSuchElementException, TimeoutException):
                logger.info("View Predictions link not found, proceeding to edit mode.")

            self.navigate_to_edit_mode()
            time.sleep(2)
            self.take_screenshot("edit_mode_after_sleep.png")

        # Load predictions from JSON
        predictions = read_predictions('data/score_predictions.json')
        if predictions is None:
            logger.error("Failed to load predictions from JSON.")
            return

        # Map teams to predictions
        team_to_prediction = self.map_teams_to_predictions(predictions)

        # Log total expected points across the six fixtures (if available)
        expected_points_values = [
            prediction.get("expected_points")
            for prediction in team_to_prediction.values()
            if prediction.get("expected_points") is not None
        ]
        if expected_points_values:
            total_expected_points = sum(expected_points_values)
            logger.info("Total expected points for this round: %.3f", total_expected_points)
        else:
            logger.info("No expected points found in predictions to sum.")

        # Adjust scores based on predictions
        self.adjust_scores(team_to_prediction)

        self._set_golden_goal('10')

        # Submit the predictions after adjustment
        self._submit_predictions()

        logger.info("Mapped teams to predictions: %s", team_to_prediction)

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
            # Check for the 'View Predictions' link
            view_predictions_link = self.driver.find_element(
                By.XPATH,
                "//a[contains(@href, '/played') and text()='View Predictions']"
            )
            if view_predictions_link:
                return True
        except NoSuchElementException:
            pass
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

    def map_teams_to_predictions(self, predictions: dict) -> dict:
        """
        Map team names from the webpage to the corresponding predictions in score_predictions.json.

        Args:
            predictions (dict): The predictions loaded from the JSON file.

        Returns:
            dict: A mapping of team names to their predictions.
        """
        assert self.driver is not None, "WebDriver not initialized."

        team_to_prediction = {}

        # Convert predictions to lowercase
        predictions_lower = [
            {k.lower(): v for k, v in prediction.items()}
            for prediction in predictions
        ]

        for i in range(1, 7):  # Iterate over the 6 games
            try:
                home_team_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//div[@data-test-id='team-container'][1]//div")
                away_team_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//div[@data-test-id='team-container'][2]//div")

                home_team = home_team_element.text.lower()
                away_team = away_team_element.text.lower()
                logger.info("Home team: %s, Away team: %s", home_team, away_team)

                # Map team names using TEAM_NAME_MAP
                home_team_mapped = TEAM_NAME_MAP.get(home_team, home_team).lower()
                away_team_mapped = TEAM_NAME_MAP.get(away_team, away_team).lower()

                # Find the corresponding prediction
                for prediction in predictions_lower:
                    if prediction.get(home_team_mapped) is not None and prediction.get(away_team_mapped) is not None:
                        team_to_prediction[(home_team, away_team)] = {
                            "home_score": prediction[home_team_mapped],
                            "away_score": prediction[away_team_mapped],
                            "probability": prediction.get("probability"),
                            "expected_points": prediction.get("expectedpoints")
                        }
                        break

            except NoSuchElementException as e:
                self.take_screenshot(f'team_mapping_error_match_{i}.png')
                logger.error("Team elements not found for match %d: %s", i, e)
                raise
        return team_to_prediction

    def adjust_scores(self, team_to_prediction: dict) -> None:
        """
        Adjust the scores for each match based on the provided predictions.

        Args:
            team_to_prediction (dict): A mapping of team names to their predicted scores.
        """
        assert self.driver is not None, "WebDriver not initialized."

        for i in range(1, 7):  # Assuming there are 6 games
            try:
                # Locate team elements
                home_team_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//div[@data-test-id='team-container'][1]//div")
                away_team_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//div[@data-test-id='team-container'][2]//div")

                home_team = home_team_element.text.lower()
                away_team = away_team_element.text.lower()

                # Get predicted scores
                prediction = team_to_prediction.get((home_team, away_team))
                if not prediction:
                    logger.warning("No prediction found for match %d: %s vs %s", i, home_team, away_team)
                    continue

                # Adjust home team score
                home_score_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//p[@data-test-id='match-team-prediction-home-score']")
                home_score = int(home_score_element.text)
                while home_score < prediction['home_score']:
                    increase_button = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//button[@data-test-id='match-team-prediction-home-increase']")
                    increase_button.click()
                    home_score += 1
                    time.sleep(0.2)
                while home_score > prediction['home_score']:
                    decrease_button = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//button[@data-test-id='match-team-prediction-home-decrease']")
                    decrease_button.click()
                    home_score -= 1
                    time.sleep(0.2)

                # Adjust away team score
                away_score_element = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//p[@data-test-id='match-team-prediction-away-score']")
                away_score = int(away_score_element.text)
                while away_score < prediction['away_score']:
                    increase_button = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//button[@data-test-id='match-team-prediction-away-increase']")
                    increase_button.click()
                    away_score += 1
                    time.sleep(0.2)
                while away_score > prediction['away_score']:
                    decrease_button = self.driver.find_element(By.XPATH, f"//div[@data-test-id='match-container-{i}']//button[@data-test-id='match-team-prediction-away-decrease']")
                    decrease_button.click()
                    away_score -= 1
                    time.sleep(0.2)

            except NoSuchElementException as e:
                logger.error("Error adjusting scores for match %d: %s", i, e)
                self.take_screenshot(f'adjust_scores_error_match_{i}.png')
                raise