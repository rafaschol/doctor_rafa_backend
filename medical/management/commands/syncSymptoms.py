import os
import requests
from django.core.management.base import BaseCommand, CommandError
from medical.models import Symptom

class Command(BaseCommand):
    help = "Sync the symptoms from the external API"

    def handle(self, *args, **options):
        API_TOKEN = os.environ["API_TOKEN"]
        url = f"{os.environ['API_URL']}/symptoms"

        response = requests.get(
            url, params={"token": API_TOKEN, "format": "json", "language": "en-gb"}
        )
        data = response.json()

        for symptom in data:
            Symptom.objects.get_or_create(id=symptom["ID"], name=symptom["Name"])