import logging
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta

from celery import Celery
from django.db import transaction
from lxml.html import HtmlElement

from exchange_watch.models import ExchangeRate

logger = logging.getLogger(__name__)
redis_dsn = 'redis://localhost:6379'

# NOTE: there's should another celery instance running in separated container
app = Celery('backend_app', backend=redis_dsn, broker='redis://localhost:6379')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, watch_exchange.s(), name='retrieve exchange rates every 10 seconds')


@app.task
def watch_exchange():
    import requests
    from io import StringIO
    from lxml import etree

    def get_rate(obj: ExchangeRate) -> None:
        url = 'https://cryptonator.com/rates/convert/?amount=1&primary={primary}&secondary={secondary}&source=liverates'
        html = requests.get(url.format(primary=obj.primary, secondary=obj.secondary)).text
        string_io = StringIO(html)

        parser = etree.HTMLParser()
        parsed = etree.parse(string_io, parser=parser)

        # NOTE: assuming that html markup won't change in 1k years
        xpath_result: HtmlElement = parsed.xpath("//h2[@class='heading-large']//strong")[0]
        value = float(xpath_result.text.strip())

        obj.rate = value

    # NOTE: select for update here? no need to wrap full logic with transaction
    with transaction.atomic():
        qs = ExchangeRate.objects \
            .filter(last_updated_date_time__lt=(datetime.now() - timedelta(seconds=10))) \
            .all()
        objs = tuple(qs)
        # NOTE: not handling neither database timeout nor network throttling/block/timeout errors here

        with ThreadPoolExecutor(max_workers=4) as executor:
            for obj in qs:
                executor.submit(get_rate, obj)

        with transaction.atomic():
            result = ExchangeRate.objects.bulk_update(objs, ['rate'])
            logger.debug('pizdets', result)
