import logging

import os

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gogetter.settings')

import django

django.setup()

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta

from celery import Celery
from django.db import transaction

from exchange_watch.models import ExchangeRate
from exchange_watch.services import ExchangeRateService

logger = logging.getLogger(__name__)
redis_dsn = f'redis://{"redis" if os.environ.get("BACKEND_ENV") == "prod" else "localhost"}:6379'

# NOTE: there's should another celery instance running in separated container
app = Celery('backend_app', backend=redis_dsn, broker=redis_dsn)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, watch_exchange.s(), name='retrieve exchange rates every 10 seconds')


@app.task
def watch_exchange():
    logger = logging.getLogger('celery')
    service = ExchangeRateService()

    def get_rate(obj: ExchangeRate) -> None:
        obj.rate = service.get_exchange_rate(obj.primary, obj.secondary)
        obj.last_update_date_time = datetime.utcnow()  # since we bulk updating, no hooks will be called for this field

    # NOTE: select for update here? no need to wrap full logic with transaction
    with transaction.atomic():
        qs = ExchangeRate.objects \
            .filter(last_update_date_time__lt=(datetime.now() - timedelta(seconds=10))) \
            .all()
        objs = tuple(qs)  # haven't done anything special, django orm caches entire qs into memory by default

        # NOTE: not handling neither database timeout nor network throttling/block/timeout errors here
        # because it requires events/queues to properly stop pool execution if any error occurred
        logger.info('Loading exchange rates. . .')
        with ThreadPoolExecutor(max_workers=4) as executor:
            for obj in objs:
                executor.submit(get_rate, obj)

        logger.info('Refreshing rates in db')
        with transaction.atomic():
            result = ExchangeRate.objects.bulk_update(objs, ['rate', 'last_update_date_time'])
            logger.debug('pizdets', result)
