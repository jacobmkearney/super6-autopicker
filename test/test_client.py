import pytest
from unittest import mock
from selenium.common.exceptions import WebDriverException, TimeoutException
from src.super6_auto_picker.client import Super6Client
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_start_browser_default_options(mock_chrome):
    # Given the start_browser method is called with default parameters
    client = Super6Client()
    
    # When the browser is initialized
    client.start_browser()
    
    # Then the WebDriver should be created with headless options
    mock_chrome.assert_called_once()
    args, kwargs = mock_chrome.call_args
    assert '--headless' in kwargs['options'].arguments

@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_login_success(mock_chrome, mock_sleep):
    # Given valid username and password are provided
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    mock_driver.find_element.return_value = mock.Mock()
    
    # When the login method is called
    client.login()
    
    # Then the user should be logged in successfully
    mock_driver.get.assert_called_with(client.base_url)
    mock_driver.find_element.assert_any_call(By.NAME, "username")
    mock_driver.find_element.assert_any_call(By.NAME, "password")
    mock_driver.find_element.assert_any_call(By.ID, "login-submit")

@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_login_no_such_element_exception(mock_chrome, mock_sleep):
    # Given login elements are missing on the page
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    mock_driver.find_element.side_effect = NoSuchElementException
    
    # When the login method is called, Then it should raise a NoSuchElementException
    with pytest.raises(NoSuchElementException):
        client.login()
        
@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_auto_pick_and_submit_not_submitted(mock_chrome, mock_sleep):
    # Given predictions have not been submitted
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    client._already_submitted = mock.Mock(return_value=False)
    client._set_predictions = mock.Mock()
    client._set_golden_goal = mock.Mock()
    client._submit_predictions = mock.Mock()
    
    # Mock start_browser to set up the WebDriver
    client.start_browser = mock.Mock()
    client.driver = mock_driver
    
    # When the auto_pick_and_submit method is called
    result = client.auto_pick_and_submit()
    
    # Then predictions should be submitted successfully
    assert result is None
    client._set_predictions.assert_called_once()
    client._set_golden_goal.assert_called_once_with('10')
    client._submit_predictions.assert_called_once()

@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_auto_pick_and_submit_already_submitted(mock_chrome, mock_sleep):
    # Given predictions have already been submitted
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    client._already_submitted = mock.Mock(return_value=True)
    
    # Mock start_browser to set up the WebDriver
    client.start_browser = mock.Mock()
    client.driver = mock_driver
    
    # When the auto_pick_and_submit method is called
    result = client.auto_pick_and_submit()
    
    # Then the method should log that predictions are already submitted
    assert result == 'already_submitted'

@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_navigate_to_edit_mode_success(mock_chrome, mock_sleep):
    # Given the edit button is present on the page
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    mock_driver.find_element.return_value = mock.Mock()
    client.driver = mock_driver

    # When the navigate_to_edit_mode method is called
    client.navigate_to_edit_mode()

    # Then the user should be navigated to the edit mode
    mock_driver.find_element.assert_called_once_with(By.ID, "js-fixtures-edit-entry")
    mock_driver.find_element.return_value.click.assert_called_once()


@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_navigate_to_edit_mode_no_such_element_exception(mock_chrome, mock_sleep):
    # Given the edit button is missing on the page
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    mock_driver.find_element.side_effect = NoSuchElementException
    client.driver = mock_driver

    # When the navigate_to_edit_mode method is called, Then it should raise a NoSuchElementException
    with pytest.raises(NoSuchElementException):
        client.navigate_to_edit_mode()


# Test Case 5.1: Accept cookies and check submission status (not submitted)
@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.EC')
@mock.patch('src.super6_auto_picker.client.WebDriverWait')
@mock.patch('src.super6_auto_picker.client.read_predictions')
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_intelligent_pick_and_submit_not_submitted(mock_chrome, mock_read_predictions, mock_webdriver_wait, mock_ec, mock_sleep):
    # Given the intelligent_pick_and_submit method is called and predictions are not submitted
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    client.driver = mock_driver
    
    # Mock cookies acceptance
    mock_cookie_element = mock.Mock()
    mock_driver.find_element.return_value = mock_cookie_element
    
    # Mock _already_submitted to return False
    client._already_submitted = mock.Mock(return_value=False)
    
    # Mock WebDriverWait and the Play For Free button
    mock_wait_instance = mock_webdriver_wait.return_value
    mock_play_for_free_button = mock.Mock()
    mock_wait_instance.until.return_value = mock_play_for_free_button
    
    # Mock EC.element_to_be_clickable
    mock_clickable_condition = mock.Mock()
    mock_ec.element_to_be_clickable.return_value = mock_clickable_condition
    
    # Mock the screenshot functionality
    client.take_screenshot = mock.Mock()
    
    # Mock predictions data and related methods
    mock_predictions = {'team1': {'home_score': 2, 'away_score': 1}}
    mock_read_predictions.return_value = mock_predictions
    client.map_teams_to_predictions = mock.Mock(return_value={'team1': mock_predictions['team1']})
    client.adjust_scores = mock.Mock()
    client._set_golden_goal = mock.Mock()
    client._submit_predictions = mock.Mock()
    
    # When the intelligent_pick_and_submit method is called
    client.intelligent_pick_and_submit()
    
    # Then cookies should be accepted
    mock_driver.find_element.assert_any_call(By.ID, "onetrust-accept-btn-handler")
    mock_cookie_element.click.assert_called_once()
    
    # And submission status should be checked
    client._already_submitted.assert_called_once()
    
    # And Play For Free button should be clicked since not submitted
    mock_webdriver_wait.assert_called_with(mock_driver, 10)
    mock_ec.element_to_be_clickable.assert_called_with(
        (By.XPATH, "//a[@data-target-id='s6-default-cta-play-btn' and text()='Play For Free']")
    )
    mock_wait_instance.until.assert_called_with(mock_clickable_condition)
    mock_play_for_free_button.click.assert_called_once()
    
    # And predictions should be processed
    mock_read_predictions.assert_called_once_with('data/score_predictions.json')
    client.map_teams_to_predictions.assert_called_once_with(mock_predictions)
    client.adjust_scores.assert_called_once()
    client._set_golden_goal.assert_called_once_with('10')
    client._submit_predictions.assert_called_once()


# Test Case 5.1b: Accept cookies and check submission status (already submitted)
@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.EC')
@mock.patch('src.super6_auto_picker.client.WebDriverWait')
@mock.patch('src.super6_auto_picker.client.read_predictions')
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_intelligent_pick_and_submit_already_submitted(mock_chrome, mock_read_predictions, mock_webdriver_wait, mock_ec, mock_sleep):
    # Given the intelligent_pick_and_submit method is called and predictions are already submitted
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    client.driver = mock_driver
    
    # Mock cookies acceptance
    mock_cookie_element = mock.Mock()
    mock_driver.find_element.return_value = mock_cookie_element
    
    # Mock _already_submitted to return True
    client._already_submitted = mock.Mock(return_value=True)
    
    # Mock WebDriverWait and the View Predictions link
    mock_wait_instance = mock_webdriver_wait.return_value
    mock_view_predictions_link = mock.Mock()
    mock_wait_instance.until.return_value = mock_view_predictions_link
    
    # Mock EC.presence_of_element_located
    mock_presence_condition = mock.Mock()
    mock_ec.presence_of_element_located.return_value = mock_presence_condition
    
    # Mock the screenshot functionality
    client.take_screenshot = mock.Mock()
    
    # Mock navigate_to_edit_mode
    client.navigate_to_edit_mode = mock.Mock()
    
    # Mock predictions data and related methods
    mock_predictions = {'team1': {'home_score': 2, 'away_score': 1}}
    mock_read_predictions.return_value = mock_predictions
    client.map_teams_to_predictions = mock.Mock(return_value={'team1': mock_predictions['team1']})
    client.adjust_scores = mock.Mock()
    client._set_golden_goal = mock.Mock()
    client._submit_predictions = mock.Mock()
    
    # When the intelligent_pick_and_submit method is called
    client.intelligent_pick_and_submit()
    
    # Then cookies should be accepted
    mock_driver.find_element.assert_any_call(By.ID, "onetrust-accept-btn-handler")
    mock_cookie_element.click.assert_called_once()
    
    # And submission status should be checked
    client._already_submitted.assert_called_once()
    
    # And View Predictions link should be clicked since already submitted
    mock_webdriver_wait.assert_called_with(mock_driver, 10)
    mock_ec.presence_of_element_located.assert_called_with(
        (By.XPATH, "//a[contains(@href, '/played') and text()='View Predictions']")
    )
    mock_wait_instance.until.assert_called_with(mock_presence_condition)
    mock_view_predictions_link.click.assert_called_once()
    
    # And navigate to edit mode should be called
    client.navigate_to_edit_mode.assert_called_once()
    
    # And predictions should be processed
    mock_read_predictions.assert_called_once_with('data/score_predictions.json')
    client.map_teams_to_predictions.assert_called_once_with(mock_predictions)
    client.adjust_scores.assert_called_once()
    client._set_golden_goal.assert_called_once_with('10')
    client._submit_predictions.assert_called_once()


# Test Case 5.1c: Play For Free button not found exception
@mock.patch('time.sleep', return_value=None)
@mock.patch('src.super6_auto_picker.client.EC')
@mock.patch('src.super6_auto_picker.client.WebDriverWait')
@mock.patch('src.super6_auto_picker.client.webdriver.Chrome')
def test_intelligent_pick_and_submit_play_for_free_not_found(mock_chrome, mock_webdriver_wait, mock_ec, mock_sleep):
    # Given the intelligent_pick_and_submit method is called but Play For Free button is not found
    client = Super6Client()
    mock_driver = mock_chrome.return_value
    client.driver = mock_driver
    
    # Mock cookies acceptance
    mock_cookie_element = mock.Mock()
    mock_driver.find_element.return_value = mock_cookie_element
    
    # Mock _already_submitted to return False
    client._already_submitted = mock.Mock(return_value=False)
    
    # Mock WebDriverWait to raise TimeoutException
    mock_wait_instance = mock_webdriver_wait.return_value
    mock_wait_instance.until.side_effect = TimeoutException
    
    # Mock EC.element_to_be_clickable
    mock_clickable_condition = mock.Mock()
    mock_ec.element_to_be_clickable.return_value = mock_clickable_condition
    
    # Mock the screenshot functionality
    client.take_screenshot = mock.Mock()
    
    # When the intelligent_pick_and_submit method is called
    # Then it should raise an Exception about Play For Free button not found
    with pytest.raises(Exception, match="Play For Free button not found, cannot proceed."):
        client.intelligent_pick_and_submit()
    
    # And cookies should be accepted
    mock_driver.find_element.assert_any_call(By.ID, "onetrust-accept-btn-handler")
    mock_cookie_element.click.assert_called_once()
    
    # And submission status should be checked
    client._already_submitted.assert_called_once()
    
    # And element_to_be_clickable should have been called for Play For Free button
    mock_ec.element_to_be_clickable.assert_called_with(
        (By.XPATH, "//a[@data-target-id='s6-default-cta-play-btn' and text()='Play For Free']")
    )
