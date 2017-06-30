from django.core.mail import send_mail
from django.conf import settings


def contact_mail(to_addr):
    message = '''

    Admcenter 收到了一封来信，请登陆后台查收

    '''
    from_addr = settings.EMAIL_HOST_USER
    send_mail('Admcenter来信提醒', message, from_addr, to_addr)