from django.urls import path
from .views import inbox, search_users, new_message, new_reply

app_name = 'inbox'

urlpatterns = [
    path('', inbox, name='inbox'),
    path('conversation/<conversation_id>/', inbox, name='inbox'),
    path('search_users/', search_users, name='search-users'),
    path('new-message/<recipient_id>', new_message, name='new_message'),
    path('new-reply/<conversation_id>', new_reply, name='new_reply'),
]
