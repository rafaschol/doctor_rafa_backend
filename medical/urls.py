from django.urls import path
from .views import SymptomList, DiagnoseView, ConfirmDiagnosisView

urlpatterns = [
    path("symptoms", SymptomList.as_view()),
    path("diagnose", DiagnoseView.as_view()),
    path("confirm-diagnosis", ConfirmDiagnosisView.as_view()),
]
