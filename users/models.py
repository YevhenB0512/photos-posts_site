from django.templatetags.static import static
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Фото')
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name="Номер телефона")
    location = models.CharField(max_length=250, blank=True, null=True, verbose_name='Город')
    bio = models.TextField(null=True, blank=True, verbose_name='О себе')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/default-avatar.jpg')
        return avatar

    @property
    def name(self):
        return self.first_name if self.first_name else self.username
