run:
	python3 manage.py runserver
makemigrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
admin:
	python3 manage.py createsuperuser
virtual:
	source venv/bin/activate
celery:
	celery -A config worker -l info
test_account:
	python3 manage.py test applications.account.tests
test_views:
	python manage.py test applications.bilets.tests
run_bot:
	python3 telebot_py.py
run_pars:
	python3 parser.py