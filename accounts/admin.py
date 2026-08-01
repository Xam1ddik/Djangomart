from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('phone', 'delivery_address', 'avatar', 'birth_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные поля', {'fields': ('phone', 'delivery_address', 'avatar', 'birth_date')}),
    )
