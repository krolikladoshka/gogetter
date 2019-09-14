from django.db import models
from django.db.models import fields


# Create your models here.
# NOTE: in real app: probably there should be a model named 'currency' for more validation & information
class CurrencyField(fields.CharField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = 32
        kwargs['null'] = False
        kwargs['blank'] = False

        super().__init__(**kwargs)


class ExchangeRate(models.Model):
    # NOTE: again, there is a lot of ways to implement a table for exchange rate montiring
    primary = CurrencyField()
    secondary = CurrencyField()

    rate = fields.FloatField()

    last_update_date_time = fields.DateTimeField(auto_now=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('primary', 'secondary'), name='db_exchange_rate_primary_secondary_unique')
        )
        index_together = (
            'primary',
            'secondary'
        )
