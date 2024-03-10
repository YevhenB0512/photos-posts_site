from django.urls import path
from .views import user_login, user_logout, user_registration, user_profile, profile_edit, profile_delete

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', user_registration, name='registration'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit', profile_edit, name='edit'),
    path('profile/<username>', user_profile, name='user_profile'),
    path('profile/delete/', profile_delete, name='delete'),
]
