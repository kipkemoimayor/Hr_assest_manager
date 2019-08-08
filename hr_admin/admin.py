from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm,CustomUserChangeForm
from .models import CustomUser,AssetModel

class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display=['name','email','username','role','company','phone','employees']

admin.site.register(CustomUser, CustomUserAdmin)
