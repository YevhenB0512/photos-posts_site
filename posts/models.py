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
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'post'
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='comments', verbose_name='Автор')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    body = models.CharField(max_length=255, verbose_name='Комментарий')
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


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='replies', verbose_name='Автор')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='Ответы')
    body = models.CharField(max_length=255, verbose_name='Комментарий')
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

