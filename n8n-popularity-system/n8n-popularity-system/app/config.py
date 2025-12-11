import os
from dotenv import load_dotenv
load_dotenv()

# API keys (put them in .env if you want real fetches)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY", "")
DISCOURSE_API_USERNAME = os.getenv("DISCOURSE_API_USERNAME", "")
DISCOURSE_BASE_URL = os.getenv("DISCOURSE_BASE_URL", "https://community.n8n.io")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./n8n_popularity.db")

# The assignment asks for US + India segmentation
COUNTRIES = ["US", "IN"]

# Search terms I used during development — tweak as needed
YOUTUBE_SEARCH_TERMS = [
    "n8n workflow",
    "n8n automation",
    "n8n slack integration",
    "n8n google sheets",
    "n8n gmail automation",
    "n8n whatsapp",
    "n8n notion automation"
]

TREND_KEYWORDS = [
    "n8n slack integration",
    "n8n gmail automation",
    "n8n google sheets integration",
    "n8n whatsapp reminders",
    "n8n notion automation",
    "n8n airtable automation",
]
