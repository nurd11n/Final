from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_code(email, activation_code):
    context = {
        'text_detail': 'Thank you for registration!',
        'email': email,
        'domain': 'http://localhost:8000',
        'activation_code': activation_code,
    }

    msg_html = render_to_string('email.html', context)
    message = strip_tags(msg_html)

    send_mail(
        'Account activation',
        message,
        'taabaldyevnurdin@gmail.com',
        [email],
        html_message=msg_html,
        fail_silently=False,
    )


def send_application_code(first_name, last_name, driver_license, email, activation_code):
    context = {
        'text_detail': 'New application',
        'first name': first_name,
        'last name': last_name,
        'driver license': driver_license,
        'email': email,
        'activation code': activation_code,
        'domain': 'http://127.0.0.1:8000/',
    }

    msg_html = render_to_string('driver_email.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Application for the job',
        message,
        'test@gmail.com',
        [email],
        html_message=msg_html,
        fail_silently=False,
    )

