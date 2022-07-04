from django.db import models
from django.contrib.auth import get_user_model


class Symptom(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    issue = models.CharField(max_length=80)
    symptoms = models.ManyToManyField(Symptom)
    date = models.DateField(auto_now_add=True)
    accuracy = models.FloatField()
    user = models.ForeignKey(
        get_user_model(), related_name="diagnostics", on_delete=models.CASCADE
    )
