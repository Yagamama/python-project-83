install: 
	pip install poetry 
	pip install gunicorn
	pip install flask
	pip install python-dotenv

dev:
	poetry run flask --app page_analyzer:app run --port 8000

lint:
	poetry run flake8 page_analyzer

port ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

mypages:
	poetry run flask --app page_analyzer:app --debug run --port 8000
