import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path=Path('.env'))

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')


def init():
    supabase = create_client(url, key)
    return supabase