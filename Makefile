requirements:
	pip freeze > requirements.txt

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

make:
	python manage.py makemigrations

mig:
	python manage.py makemigrations
	python manage.py migrate
	@echo ************  Successfully made migrations and migrated  ************

admin:
	python manage.py createsuperuser