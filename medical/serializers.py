from rest_framework import serializers
from .models import Symptom, Diagnosis


class SymptomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Symptom
        fields = ["id", "name"]


class DiagnosisSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)

    class Meta:
        model = Diagnosis
        fields = ["id", "issue", "symptoms", "accuracy", "date"]
