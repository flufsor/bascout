import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for bascout.
    """
    def __init__(self):
        self.maxmind_id = os.getenv("MAXMIND_ID", "")
        self.maxmind_key = os.getenv("MAXMIND_LICENSE_KEY", "")