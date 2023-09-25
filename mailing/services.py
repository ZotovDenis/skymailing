import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog

logger = logging.getLogger(__name__)


def send_message(mailing_settings):
    clients = mailing_settings.clients.all()
    clients_list = [client.email for client in clients]

    server_response = 'None'
    status = MailingLog.STATUS_FAILED

    try:
        letter = send_mail(
            subject=mailing_settings.message.message_title,
            message=mailing_settings.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_list,
        )

        if letter:
            status = MailingLog.STATUS_OK
            server_response = 'Успешно'

    except SMTPException as e:
        server_response = str(e)
        logger.error(f'Исключение SMTPException: {e}')
    else:
        logger.info('Успешно')

    if server_response:
        logger.info(f'Ответ сервера: {server_response}')

    MailingLog.objects.create(
        settings=mailing_settings,
        status=status,
        response=server_response
    )
