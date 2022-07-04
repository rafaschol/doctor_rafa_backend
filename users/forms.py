from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
