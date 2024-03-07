from django.urls import path
from .views import home, post_create, post_delete, post_edit, post_detail

app_name = 'posts'

urlpatterns = [
    path('', home, name='home'),
    path('category/<tag>/', home, name='by_category'),
    path('post/create/', post_create, name='create'),
    path('post/<pk>/', post_detail, name='detail'),
    path('post/edit/<pk>/', post_edit, name='edit'),
    path('post/delete/<pk>/', post_delete, name='delete'),
]
