# from pathlib import Path
import os
# import environ
import requests
import django

# Setting up Env
# env = environ.Env()
# BASE_DIR = Path(__file__).resolve().parent.parent
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from medical.models import Symptom

API_TOKEN = os.environ["API_TOKEN"]
url = f"{os.environ['API_URL']}/symptoms"

response = requests.get(
    url, params={"token": API_TOKEN, "format": "json", "language": "en-gb"}
)
data = response.json()

for symptom in data:
    Symptom.objects.get_or_create(id=symptom["ID"], name=symptom["Name"])
