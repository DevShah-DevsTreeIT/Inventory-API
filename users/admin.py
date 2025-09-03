from django.contrib import admin
from .models import User   # import your model here


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "password", "auth_token", "created_at")

