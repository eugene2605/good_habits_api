from django.contrib import admin

from users.models import User


@admin.register(User)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'city', 'avatar', 'telegram_id')
