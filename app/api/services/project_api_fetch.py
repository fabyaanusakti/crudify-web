import requests
from app.models import AppConfig

def fetch():
    try:
        config = AppConfig.load()
        if not hasattr(config, 'projek_api_endpoint'):
            default_endpoint = 'https://michaelbriant.pythonanywhere.com/api/proyek/'
            print(f"Warning: api_endpoint not found in AppConfig, using default: {default_endpoint}")
            response = requests.get(default_endpoint)
        else:
            response = requests.get(config.projek_api_endpoint)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching projects: {e}")
        return None
