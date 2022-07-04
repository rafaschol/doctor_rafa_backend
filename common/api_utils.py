import os
import environ
import requests
from django.core.cache import cache

env = environ.Env()
if os.environ.get("DEBUG", True):
    environ.Env.read_env(".env")


def get_api_key():
    url = f"{env('API_AUTH_URL')}/login"
    response = requests.post(
        url, headers={"Authorization": f"Bearer {env('API_AUTH_AUTHORIZATION')}"}
    )
    data = response.json()
    API_TOKEN = data["Token"]
    cache.set("API_KEY", API_TOKEN)
    return API_TOKEN
