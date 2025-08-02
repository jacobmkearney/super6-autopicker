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
- **Next:**
  - Add logic to programmatically confirm successful login (e.g., check URL or page content).
  - Handle login errors and log them.
  - Proceed to game data retrieval and subsequent steps.

## 3. Game Data Retrieval
- Identify how to fetch weekly fixtures (API endpoint or scraping)
- Implement fixture retrieval in `client.py`
- Parse and structure fixture data for use in auto-picking

## 4. Auto-Pick Logic
- Design the auto-pick algorithm (random, weighted, or user-defined)
- Implement the algorithm in a dedicated module or within `client.py`
- Allow for configuration or extension of pick logic

## 5. Submission of Picks
- Analyze how picks are submitted (API or form POST)
- Implement pick submission in `client.py`
- Confirm and log successful submission
- Handle and log errors

## 6. Scheduling
- Implement scheduling in `scheduler.py`:
  - Use cron (document setup) or Python's `schedule` library
  - Ensure script runs daily at the desired time
- Implement logging and error reporting (to file, email, or terminal)

## 7. Testing
- Add unit and integration tests in `src/tests/`
- Test login, data retrieval, pick logic, and submission
- Test full workflow end-to-end

## 8. Documentation
- Maintain this plan in `PLAN.md` and update as needed
- Document setup, usage, and troubleshooting in `README.md`
- Add code comments and docstrings throughout the codebase

---

### Next Steps
- [ ] Add logic to confirm successful login (programmatically)
- [ ] Handle login errors and log them
- [ ] Proceed with game data retrieval and subsequent steps 