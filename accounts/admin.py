from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'name', 'age', 'gender', 'phone_number')
    list_filter = ('role', 'gender')
    search_fields = ('email', 'name', 'phone_number')
