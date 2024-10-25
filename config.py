from dotenv import load_dotenv
import os

load_dotenv()

def load_config():
    # You can still use your JSON config if needed
    # Just ensure you also pull from environment variables
    return {
        'api_key': os.getenv('API_KEY'),
        'db_path': os.getenv('DATABASE_URL'),
        'interval': int(os.getenv('FETCH_INTERVAL', 300)) 
    }
