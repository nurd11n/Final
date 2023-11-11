from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_application_email(first_name, last_name, driver_license, car, email, activation_code):
    context = {
        'text_detail': 'New application',
        'first name': first_name,
        'last name': last_name,
        'license': driver_license,
        'car': car,
        'email': email,
        'activation code': activation_code,
        'domain': 'http://localhost:8000',
    }

    msg_html = render_to_string('email.html', context)
    message = strip_tags(msg_html)
    send_mail(
        'Application for the job',
        message,
        'test@gmail.com',
        ['taabaldyevnurdin@gmail.com'],
        html_message=msg_html,
        fail_silently=False,
    )

# def send_confirm(first_name, last_name, email):
#     ...
