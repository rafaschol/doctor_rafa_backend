import os
import environ
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Symptom, Diagnosis
from .serializers import SymptomSerializer, DiagnosisSerializer
import requests
from django.core.cache import cache
from common.api_utils import get_api_key

env = environ.Env()
if os.environ.get("DEBUG", True):
    environ.Env.read_env(".env")


class SymptomList(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


def process_diagnosis(apiData):
    data = []
    for result in apiData:
        issue = result["Issue"]
        data.append(
            {
                "id": issue["ID"],
                "name": issue["Name"],
                "accuracy": issue["Accuracy"],
                "ranking": issue["Ranking"],
            }
        )
    return Response(data, status=200)


class DiagnoseView(APIView):
    def get(self, request):
        symptoms = request.query_params.get("symptoms")
        user = self.request.user

        url = f"{env('API_URL')}/diagnosis"
        API_TOKEN = cache.get("API_KEY") if cache.get("API_KEY") else get_api_key()

        apiResponse = requests.get(
            url,
            params={
                "token": API_TOKEN,
                "symptoms": symptoms,
                "gender": user.get_gender_display().lower(),
                "year_of_birth": user.birth_date.year,
                "format": "json",
                "language": "en-gb",
            },
        )

        if apiResponse.status_code == requests.codes.ok:
            return process_diagnosis(apiResponse.json())
        else:
            API_TOKEN = get_api_key()
            apiResponse = requests.get(
                url,
                params={
                    "token": API_TOKEN,
                    "symptoms": symptoms,
                    "gender": user.get_gender_display().lower(),
                    "year_of_birth": user.birth_date.year,
                    "format": "json",
                    "language": "en-gb",
                },
            )
            return process_diagnosis(apiResponse.json())


class ConfirmDiagnosisView(generics.CreateAPIView):
    serializer_class = DiagnosisSerializer

    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, symptoms=self.request.data["symptoms"])
