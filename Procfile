web: gunicorn config.wsgi:application
worker: celery worker --app=danibraz.taskapp --loglevel=info
