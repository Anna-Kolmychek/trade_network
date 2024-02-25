from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']
    list_display_links = ['email']
