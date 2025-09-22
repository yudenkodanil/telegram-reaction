import os
from pathlib import Path

class Config:
    SESSION_FILE = Path("session/my_session")
    API_ID = os.getenv("TG_API_ID")
    API_HASH = os.getenv("TG_API_HASH")
    CHANNELS = os.getenv("TG_CHANNELS", "").split(",")
    REACTION = os.getenv("TG_REACTION", "👍")
