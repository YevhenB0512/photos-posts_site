from django.urls import path
from .views import user_login, user_logout, user_registration, user_profile, profile_edit

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', user_registration, name='registration'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit', profile_edit, name='edit'),
]
