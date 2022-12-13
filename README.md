flask-blueprint
===============

A dummy Flask app used to showcase how a few different concepts and building blocks come together. Features:

* Flask app creation using the [application factory pattern](https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/).
* App modularity with [Flask Blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/).
* All config separate from app logic; config storage in [environment variables](https://12factor.net/config)
* Use of [Celery](https://docs.celeryq.dev/en/stable/) as a distributed task queue for asynchronous tasks.
* Use of [Redis](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html) as both the message broker and the results backend for Celery.
* Use of [Celery flower](https://flower.readthedocs.io/en/latest/), a Celery monitoring tool.
* db integration, currently with sqlite3.
* [SQLAlchemy](https://www.sqlalchemy.org/), an ORM (Object Relational Mapper) for Python.
* [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate/blob/main/README.md), an extension that handles SQLAlchemy database migrations using [Alembic](https://alembic.sqlalchemy.org/en/latest/).

Current Status
--------------

The app is currently under refactoring. The next step is to move the creation of the Celery instance to a [make_celery()](https://flask.palletsprojects.com/en/2.2.x/patterns/celery/)factory function inside `api.__init__.py`, and the Celery config to `api.config.py`.

The dev experience is not very user-friendly right now.
We will move to docker-compose so that we don't have to manually start and manage all the different services (Flask, redis, flower, db...)

We may also move from `pip` to [`poetry`](https://python-poetry.org/docs/) for dependency management.

Another thing that's currently missing is tests (with e.g. Pytest), linters, formatters, and other code quality checkers, as well as a CI pipeline that uses these.

Running the app
---------------

Clone the app and cd into the root directory.

Create a virtual environment through your preferred method (pyenv-virtualenv, venv...) and activate it.

Install the dependencies:

    pip install -r requirements.txt

* Make sure you have a running Redis instance, either locally, or in a Docker container.

Locally:

    $ redis-server
    $ redis-cli ping  # Test that it's up and running
    PONG

With Docker:

    $ docker run -p 6379:6379 --name my-redis -d redis
    $ docker exec -it my-redis redis-cli ping
    PONG

In another terminal window/tab, start the Celery worker:

    celery -A app.celery worker --loglevel=info

In a third terminal window/tab, start Celery flower:

    celery -A app.celery flower --port=5555

You can now navigate to <http://localhost:5555> to view the flower dashboard.

In your first terminal window/tab, start a flask shell:

    FLASK_APP=app.py flask shell

Now you can send a task to celery:

```python
>>> from app import divide
>>> task = divide.delay(10, 2)
```

It should appear on the flower dashboard (you may have to refresh the page), and in the celery worker logs.

You can also set up and explore the database (not needed for celery-redis):

    $ FLASK_APP=app.py flask db upgrade

This will apply the initial migration and create the `Users` table. You can now play with it in the flask shell:

```python
>>> from api.users.models import User
>>> user = User(username='geekLeek007', email='geek@leek.com')
>>> db.session.add(user)
>>> db.session.commit()
>>> User.query.first().username
'geekLeek007'
```