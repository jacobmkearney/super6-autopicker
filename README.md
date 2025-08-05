# super6-autopicker

Automated completion of SkyBet's Super6

## Setup & Usage

### 1. Install dependencies

It is recommended to use a Python virtual environment for isolation:

```
python3 -m venv .venv
source .venv/bin/activate
```

Then, install uv (if you don't have it):

```
pip install uv
```

Now install all dependencies from pyproject.toml using uv:

```
uv pip install .
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

### 4. Run the autopicker

Run the script using Python 3:

```
python3 main.py
```

This will:
- Launch a headless Chrome browser
- Attempt to log in to Super 6
- Complete the full autopicker process (including making and submitting picks)
- Save a screenshot as `submission_result.png` in the project root

Check `submission_result.png` to confirm the process was successful.

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
   0 12 * * * /path/to/your/project/.venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/cron.log 2>&1
   ```
   - Replace the paths with your own project and Python locations.
   - All output and errors will be appended to `cron.log` in your project folder.

5. **Save and exit the editor.**

#### Customizing the Schedule
You can adjust the schedule to fit your needs. For example:
- **Every Tuesday and Friday at 12:00 PM (for midweek and weekend fixtures):**
  ```
  0 12 * * 2,5 /path/to/your/project/.venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/cron.log 2>&1
  ```
  (Here, `2,5` means Tuesday and Friday. See [crontab.guru](https://crontab.guru/) for help with cron syntax.)

**To check the log output:**
```sh
tail -n 50 /path/to/your/project/cron.log
```
