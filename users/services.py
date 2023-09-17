from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


def send_verification_email(email, verification_token):
    subject = 'Подтверждение почты'
    message = f'Для завершения подтверждения почты укажите на сайте Ваш код верификации: {verification_token}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def send_password(email):
    User = get_user_model()

    try:
        user = User.objects.get(email=email)

        new_password = get_random_string(length=16)
        user.set_password(new_password)
        user.save()

        subject = 'Вы запросили смену пароля'
        message = f'Ваша почта была указана для получения нового пароля для входа. Ваш новый пароль: {new_password}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return True
    except User.DoesNotExist:
        return False