Celery
=========
We are using version 4+. Main config is in `project/celery.py`. See supervisor conf files inside `conf` for example commands to run celery beat scheduler (we're using the db based scheduler) and celery workers. Also see setting `BROKER_URL` for required configuration of rabbitmq broker. Hint: use `rabbitmqctl` or management plugin (web interface) to create user with password and required vhost.
