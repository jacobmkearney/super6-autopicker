# Super 6 Auto-Picker: Project Plan

## 1. Project Setup (Completed)
- Python project initialized with virtual environment
- Git repository set up
- Project structure under `src/super6_auto_picker/`
- Configuration loads credentials from `.env` via `config.py`

## 2. Authentication & Login Flow
- **Selenium-based login implemented in `client.py` using Chrome.**
- The login process now:
  1. Opens a headless Chrome browser and navigates to the Super 6 play URL.
  2. Waits for redirect to the SkyBet login page.
  3. Automatically accepts the cookie consent overlay if present (clicks the 'Allow All Cookies' button).
  4. Fills in the username and PIN fields.
  5. Clicks the login button.
  6. Waits for redirect and login to complete.
  7. Takes a screenshot (`login_result.png`) after login for verification.
  8. Accepts cookies again if prompted after redirect to super6.skysports.com.

## 3. Game Data Retrieval & Auto-Pick Logic (Now Automated)
- After login and cookie acceptance:
  1. Navigate to https://super6.skysports.com/play
  2. For each match prediction controller, increase the home team score by one (so all home teams are set to win 1-0)
  3. Enter '10' into the golden goal input
  4. Click the 'SUBMIT PREDICTIONS' button
  5. Take a screenshot after submission for verification

## 4. Submission of Picks
- Submission is now automated as part of the Selenium workflow
- Confirm and log successful submission (via screenshot or page check)
- Handle and log errors

## 5. Scheduling
- Implement scheduling in `scheduler.py`:
  - Use cron (document setup) or Python's `schedule` library
  - Ensure script runs daily at the desired time
- Implement logging and error reporting (to file, email, or terminal)

## 6. Testing
- Add unit and integration tests in `src/tests/`
- Test login, data retrieval, pick logic, and submission
- Test full workflow end-to-end

## 7. Documentation
- Maintain this plan in `PLAN.md` and update as needed
- Document setup, usage, and troubleshooting in `README.md`
- Add code comments and docstrings throughout the codebase

---

### Next Steps
- [ ] Add logic to confirm successful submission (programmatically)
- [ ] Handle submission errors and log them
- [ ] Proceed with scheduling and further automation 