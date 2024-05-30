install: 
	pip install poetry 
	pip install gunicorn
	pip install flask
	pip install dotenv

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

port ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app
