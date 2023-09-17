from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_staff', 'first_name', 'last_name', 'email', 'phone', 'is_verificated')
    list_filter = ('is_verificated', 'is_staff')
    search_fields = ('email', 'phone', 'first_name', 'last_name')
