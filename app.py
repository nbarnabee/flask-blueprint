from celery import Celery
from flask_restful import Api

from api import create_app
from api.routes.index import Index

app = create_app()
api = Api(app)


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)

api.add_resource(Index, "/")
# register the route we've importted

@celery.task
def divide(x, y):
    import time

    time.sleep(5)
    return x / y
