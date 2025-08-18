# super6-autopicker

Automated completion of SkyBet's Super6

## Setup & Usage

### 1. Install dependencies

Use a Python virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install uv:

```
pip install uv
```

Install all dependencies from pyproject.toml:

```
uv pip install .
```

### 2. Requirements
- Python 3.12+
- Google Chrome browser installed
- ChromeDriver (compatible with your Chrome version; Selenium will attempt to auto-download if not present)

### 3. Configure credentials
Create a `.env` file in the project root with your Super 6 username, PIN, and The Odds API key:

```
USERNAME=your_username
PIN=your_pin
ODDS_API_KEY=your_api_key
```

### 4. Run the autopicker

#### Option 1: Basic Submission

```
python3 main.py
```

This will:
- Launch a headless Chrome browser
- Attempt to log in to Super 6
- Submit a default prediction of 1-0 for the home team if no previous submission exists

#### Option 2: Optimized Prediction

To use the optimized prediction feature, which scrapes data and predicts the correct result, run:

```
python3 main.py --optimise
```

This will:
- Launch a headless Chrome browser
- Attempt to log in to Super 6
- Fetch odds data using The Odds API
- Predict the most likely score
- Submit the predicted score

### 5. Scheduling Automatic Daily Runs

To run the autopicker automatically on a schedule (e.g., every day at midday), you can use `cron` (available on macOS and Linux):

1. **Find your Python executable in your virtual environment**

   Activate your virtual environment and run:
   ```sh
   which python
   ```
   Note the full path (e.g., `/path/to/your/project/.venv/bin/python`).

2. **Find the full path to your `main.py` script**

   For example: `/path/to/your/project/main.py`

3. **Open your crontab for editing:**
   ```sh
   crontab -e
   ```

4. **Add a line to schedule your script.**
   For example, to run every day at 12:00 PM (midday):
   ```
   0 12 * * * /path/to/your/project/.venv/bin/python /path/to/your/project/main.py --optimise >> /path/to/your/project/cron.log 2>&1
   ```
   - Replace the paths with your own project and Python locations.
   - All output and errors will be appended to `cron.log` in your project folder.

5. **Save and exit the editor.**
