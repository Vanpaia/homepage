import requests
from config import SECRET_KEY

BASE_URL = "http://localhost:5000/api"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": SECRET_KEY
}

response = requests.delete(f"{BASE_URL}/projects/3", headers=headers)
print(response.json())
