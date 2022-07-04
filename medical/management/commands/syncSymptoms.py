import os
import environ
import requests
from django.core.management.base import BaseCommand
from django.core.cache import cache
from medical.models import Symptom
from common.api_utils import get_api_key

# Set up env
env = environ.Env()
if os.environ.get("DEBUG", True):
    environ.Env.read_env(".env")


def load_symptoms(symptoms):
    for symptom in symptoms:
        Symptom.objects.get_or_create(id=symptom["ID"], name=symptom["Name"])


class Command(BaseCommand):
    help = "Sync the symptoms from the external API"

    def handle(self, *args, **options):
        # Get API token from cache, or get a new API token if not found
        url = f"{env('API_URL')}/symptoms"
        API_TOKEN = cache.get("API_KEY") if cache.get("API_KEY") else get_api_key()

        # Do main request
        response = requests.get(
            url, params={"token": API_TOKEN, "format": "json", "language": "en-gb"}
        )

        # Check if request is OK. If not, generate a new API token and try again
        if response.status_code == requests.codes.ok:
            load_symptoms(response.json())

        else:
            API_TOKEN = get_api_key()
            response = requests.get(
                url, params={"token": API_TOKEN, "format": "json", "language": "en-gb"}
            )

            load_symptoms(response.json())
