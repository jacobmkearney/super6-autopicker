from dotenv import load_dotenv
import os

load_dotenv() 

USERNAME = os.getenv("USERNAME")
PIN = os.getenv("PIN")
BASE_URL = "https://super6.skysports.com/play"
DEFAULT_SCORE = (1, 0)
