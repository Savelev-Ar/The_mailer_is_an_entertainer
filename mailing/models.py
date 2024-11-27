from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Ф.И.О.'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='контактный email'
    )
    comment = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='комментарий'
    )

    def __str__(self):
        return f'{self.email} ({self.name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['name']


class Message(models.Model):
    topic = models.CharField(
        max_length=200,
        verbose_name='тема'
    )
    body = models.TextField(
        verbose_name='сообщение'
    )

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['topic']


class Settings(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    STATUS_SET = (
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
        (COMPLETED, 'завершена'),
    )
    FREQUENCY_SET = (
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц'),
    )
    description = models.CharField(
        max_length=200,
        verbose_name='заголовок',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_SET,
        default=CREATED,
        verbose_name='статус')
    date_start = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        verbose_name='дата и время первой отправки'
    )
    frequency = models.CharField(
        max_length=15,
        choices=FREQUENCY_SET,
        verbose_name='периодичность'
    )
    clients = models.ManyToManyField(
        Client,
        related_name='clients',
        verbose_name='клиенты'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name="сообщение")

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылок'
        ordering = ['date_start']


class Attempt(models.Model):
    last_datetime = models.DateTimeField(
        verbose_name='дата и время последней попытки'
    )
    is_successfully = models.BooleanField(
        default=False,
        verbose_name='статус попытки'
    )
    settings = models.ForeignKey(
        Settings,
        on_delete=models.CASCADE,
        null=True,
        related_name='attempts',
        verbose_name=' попытка рассылки'
    )
    response = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ответ сервера'
    )

    def __str__(self):
        return f'{self.settings}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
