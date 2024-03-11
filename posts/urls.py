from django.urls import path
from .views import (home, post_create, post_delete, post_edit, post_detail, sent_comment,
                    delete_comment, sent_reply, delete_reply, like_post)

app_name = 'posts'

urlpatterns = [
    path('', home, name='home'),
    path('category/<tag>/', home, name='by_category'),
    path('post/create/', post_create, name='create'),
    path('post/<pk>/', post_detail, name='detail'),
    path('post/<pk>/like', like_post, name='like_post'),
    path('post/edit/<pk>/', post_edit, name='edit'),
    path('post/delete/<pk>/', post_delete, name='delete'),
    path('sent-comment/<pk>', sent_comment, name='sent_comment'),
    path('comment/delete/<pk>', delete_comment, name='delete_comment'),
    path('sent-reply/<pk>', sent_reply, name='sent_reply'),
    path('reply/delete/<pk>', delete_reply, name='delete_reply'),
]
