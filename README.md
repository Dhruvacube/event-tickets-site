# Self Hosting Guide
To run this app you need you need `python 3.9.9`, `postgres`, `redis`, `rabbitmq`, `memchache`, `scheduler`
Rename [example.env](/example.env) to `.env` and then set the values in `.env` as stated in the [example.env](/example.env) file.

See the uvicorn commands from [Dockerfile](/DOCKERFILE) or gunicorn commands from [Procfile](/Procfile)
or run using the `python manage.py runserver` command.

# Hosting on Heroku and Connecting it with domain

