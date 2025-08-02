# super6-autopicker

Automated completion of SkyBet's Super6

## Setup & Usage

### 1. Install dependencies

With your virtual environment activated, install all dependencies from pyproject.toml:

```
pip install -e .
```

### 2. Requirements
- Python 3.12+
- Google Chrome browser installed
- ChromeDriver (compatible with your Chrome version; Selenium will attempt to auto-download if not present)

### 3. Configure credentials
Create a `.env` file in the project root with your Super 6 username and PIN:

```
USERNAME=your_username
PIN=your_pin
```

### 4. Run the login test

```
python main.py
```

This will:
- Launch a headless Chrome browser
- Attempt to log in to Super 6
- Save a screenshot as `login_result.png` in the project root

Check `login_result.png` to confirm the login was successful.

---

For further development, see `PLAN.md` for the project roadmap.
