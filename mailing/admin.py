from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'comment')
    search_fields = ('email', 'first_name', 'last_name', 'comment')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_title', 'message')
    search_fields = ('message_title', 'message')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'period', 'status', 'message')
    list_filter = ('period', 'status')
    search_fields = ('message', )

