from django.contrib import admin
from .models import Post, Tag, Comment, Reply, LikedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'created')


@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'slug')


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'parent_post', 'body', 'created', 'id')


@admin.register(Reply)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'parent_comment', 'body', 'created', 'id')
