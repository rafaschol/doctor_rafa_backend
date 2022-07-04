from pathlib import Path
import os
import environ
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Symptom, Diagnosis
from .serializers import SymptomSerializer, DiagnosisSerializer
import requests

# Setting up Env
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class SymptomList(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class DiagnoseView(APIView):
    def get(self, request):
        symptoms = request.query_params.get("symptoms")
        user = self.request.user

        API_TOKEN = env("API_TOKEN")
        url = f"{env('API_URL')}/diagnosis"

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
        apiData = apiResponse.json()

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


class ConfirmDiagnosisView(generics.CreateAPIView):
    serializer_class = DiagnosisSerializer

    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, symptoms=self.request.data["symptoms"])
