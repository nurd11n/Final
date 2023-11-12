from config.celery import app
from .utils import send_activation_code, send_application_email


@app.task
def send_activation_code_celery(email, activation_code):
    send_activation_code(email, activation_code)

@app.task
def send_application_celery(first_name, last_name, driver_license, car, email, activation_code):
    send_application_email(first_name, last_name, driver_license, car, email, activation_code)