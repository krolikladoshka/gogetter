from io import StringIO
from typing import Union, List

import requests
from lxml import etree
from lxml.html import HtmlElement


class ExchangeRateNotFound(Exception):
    pass


class ExchangeRateService:
    def get_exchange_rate(self, primary: str, secondary: str) -> float:
        url = 'https://cryptonator.com/rates/convert/?amount=1&primary={primary}&secondary={secondary}&source=liverates'
        try:
            response: requests.Response = requests.get(url.format(primary=primary, secondary=secondary))
            response.raise_for_status()
        except requests.HTTPError as e:
            # all this logic was unnecessary, because target website awlays returns HTTP OK with HTTP 404 body. . .
            if e.response.status_code == 404:
                raise ExchangeRateNotFound
            raise e

        html = response.text
        string_io = StringIO(html)

        parser = etree.HTMLParser()
        parsed = etree.parse(string_io, parser=parser)

        # NOTE: assuming that html markup won't change in 1k years
        xpath_result: List[Union[HtmlElement, str]] = parsed.xpath("//h2[@class='heading-large']//strong")

        if xpath_result:
            return float(xpath_result[0].text.strip())
        # trying to save everything i've done before i learned about always-ok responses
        raise ExchangeRateNotFound
