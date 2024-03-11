import uuid

from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='url')
    image = models.FileField(upload_to='icons/', null=True, blank=True)

    class Meta:
        db_table = 'tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False, verbose_name='ID')
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    image = models.ImageField(upload_to='posts_images', verbose_name='Изображение')
    body = models.TextField(verbose_name='Запись')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='likedposts', through='LikedPost')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'post'
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Запись')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'likedpost'
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='comments', verbose_name='Автор')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    body = models.CharField(max_length=255, verbose_name='Комментарий')
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False, verbose_name='ID')

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created', )

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[0:30]}'
        except:
            return f'Автор удвлен: {self.body[0:30]}'


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'likedcomment'
        verbose_name = 'Понравившийся комментарий'
        verbose_name_plural = 'Понравившиеся комментарии'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username}: {self.comment.body[:30]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='replies', verbose_name='Автор')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='Ответы')
    body = models.CharField(max_length=255, verbose_name='Комментарий')
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False, verbose_name='ID')

    class Meta:
        db_table = 'reply'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('-created', )

    def __str__(self):
        try:
            return f'{self.author.username}: {self.body[0:30]}'
        except:
            return f'Автор удвлен: {self.body[0:30]}'


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='Ответ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'likedreply'
        verbose_name = 'Понравившийся ответ'
        verbose_name_plural = 'Понравившиеся ответы'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username}: {self.reply.body[:30]}'
