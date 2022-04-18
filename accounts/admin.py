from django.contrib import admin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login')