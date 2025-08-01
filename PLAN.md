# Super 6 Auto-Picker: Project Plan

## 1. Project Setup (Completed)
- Python project initialized with virtual environment
- Git repository set up
- Project structure under `src/super6_auto_picker/`
- Configuration loads credentials from `.env` via `config.py`

## 2. Authentication & Login Flow
- Analyze the Super 6 login process:
  - Use browser dev tools to inspect login requests (form POST, API, or JS-based?)
  - Identify required fields (username, PIN, CSRF tokens, etc.)
  - Determine if login can be scripted (requests) or needs a headless browser (Selenium)
- Implement login in `client.py`:
  - Handle session management (cookies, tokens)
  - Store and refresh session as needed
  - Log errors and failed attempts
- **Document findings and implementation details here as we proceed.**

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
- [ ] Analyze and document the Super 6 login flow in detail
- [ ] Implement and test login functionality
- [ ] Proceed with game data retrieval and subsequent steps 