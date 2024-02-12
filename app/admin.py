from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from app.models import CustomUser
from app import __version__

admin.AdminSite.site_header = f"Tiny Warehouse ({__version__})"


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'is_staff', 'is_active',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )

    search_fields = DjangoUserAdmin.search_fields + ('email',)
    ordering = ('email',)
