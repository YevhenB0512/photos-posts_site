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
