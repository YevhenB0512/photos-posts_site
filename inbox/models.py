import uuid

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

from users.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',
                               verbose_name='Отправитель')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE,
                                     related_name='messages', verbose_name='Чат')
    body = models.TextField(verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'inboxmessage'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-created', )

    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f'[{self.sender.username} : {time_since} назад]'

    @property
    def body_decrypted(self):
        f = Fernet(settings.ENCRYPT_KEY)
        message_decrypted = f.decrypt(self.body)
        message_decoded = message_decrypted.decode('utf-8')
        return message_decoded


class Conversation(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False, verbose_name='ID')
    participants = models.ManyToManyField(User, related_name='conversations', verbose_name='Участники')
    lastmessage_created = models.DateTimeField(default=timezone.now, verbose_name='Недавнее')
    is_seen = models.BooleanField(default=False, verbose_name='Просмотрено')

    class Meta:
        db_table = 'conversation'
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        ordering = ('-lastmessage_created', )

    def __str__(self):
        user_names = [user.username for user in self.participants.all()]
        user_names = ', '.join(user_names)
        return user_names
