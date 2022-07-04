from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import NewUserCreationForm, NewUserChangeForm
from .models import User


class NewUserAdmin(UserAdmin):
    add_form = NewUserCreationForm
    form = NewUserChangeForm
    model = User
    # list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')


admin.site.register(User, NewUserAdmin)
