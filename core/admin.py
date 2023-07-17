from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username',)
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
