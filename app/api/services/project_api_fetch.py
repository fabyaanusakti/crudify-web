import requests

PROJECT_API_URL = 'https://faizbyaan.pythonanywhere.com/api/projek/'

def fetch():
    try:
        response = requests.get(PROJECT_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching projects: {e}")
        return None