from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # <-- ЭТОТ ИМПОРТ КРИТИЧЕСКИ ВАЖЕН!

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

# Регистрируем кастомного пользователя с кастомной админкой
admin.site.register(User, CustomUserAdmin)
