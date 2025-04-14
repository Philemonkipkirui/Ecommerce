from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Custom form for adding users
    model = CustomUser

    list_display = ('username', 'email', 'phone_number', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('phone_number', 'user_type')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('phone_number', 'user_type')}),
    )

    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
