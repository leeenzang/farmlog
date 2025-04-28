from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'nickname', 'is_active', 'is_staff')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'nickname')
    ordering = ('id',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('nickname',)}),
    )