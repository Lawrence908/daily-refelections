import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')

DATA_DIR = os.getenv('DATA_DIR', 'data')

# Data file paths
QUOTES_FILE = os.path.join(DATA_DIR, 'quotes.json')
STOIC_QUOTES_FILE = os.path.join(DATA_DIR, 'stoic_quotes.json')
ENTRIES_FILE = os.path.join(DATA_DIR, 'user_entries.json')