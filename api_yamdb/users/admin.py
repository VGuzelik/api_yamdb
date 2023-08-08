from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'bio',
        'role',
        'confirmation_code',
    )
    list_editable = ('email', 'role',)
    search_fields = ('role', 'username', 'email',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User)
