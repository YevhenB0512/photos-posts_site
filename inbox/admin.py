from django.contrib import admin
from .models import InboxMessage, Conversation


@admin.register(InboxMessage)
class InboxMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'conversation', 'body', 'created')
    readonly_fields = ('id', 'sender', 'conversation', 'body', 'created')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lastmessage_created', 'is_seen')
