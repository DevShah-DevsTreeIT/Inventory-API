from django.contrib import admin
from .models import User   # import your model here


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_email", "user_password", "auth_token", "created_date")

