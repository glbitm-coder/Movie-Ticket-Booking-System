from application import create_app
from application.celery_worker import make_celery

app = create_app()

app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/1',
        CELERY_RESULT_BACKEND='redis://localhost:6379/2'
    )
celery = make_celery(app)
from application.tasks import *

if __name__ == '__main__':
    app.run(debug=True)