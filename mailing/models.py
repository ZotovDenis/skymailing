from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта')
    first_name = models.CharField(**NULLABLE, verbose_name='Имя', max_length=150)
    last_name = models.CharField(**NULLABLE, verbose_name='Фамилия', max_length=150)
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец клиента', default=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    message_title = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.message_title}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    time = models.TimeField(verbose_name='Время')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='Получатели рассылки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.time} / {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
