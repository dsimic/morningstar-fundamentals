# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from fundamentals.mstar_util import get_requests, MSTAR_PERIOD_IDS, get_symbols
from fundamentals.items import CashFlowItem
import json


class CashflowSpider(scrapy.Spider):
    name = "cashflow"
    allowed_domains = ["morningstar.com"]

    def __init__(self, settings):
        self.my_settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def start_requests(self):
        report_type = 'cf'
        symbols = get_symbols(self.my_settings['SYMBOL_FILE'])
        requests = get_requests(self.parse, symbols, "A", report_type)
        requests += get_requests(self.parse, symbols, "Q", report_type)
        return requests

    def parse(self, response):
        response = response.replace(
            body=json.loads(response.body)['result'])
        hxs = Selector(response)
        for period_id in MSTAR_PERIOD_IDS:
            yield self.parse_period(hxs, period_id, response.meta)

    def parse_period(self, hxs, period_id, meta):
        item = CashFlowItem()
        item['symbol'] = meta['symbol']
        item['freq'] = meta['freq']
        item['cash_from_operating_activities'] = \
            self.parse_generic(hxs, period_id, 1)
        item['cash_from_investment_activities'] = \
            self.parse_generic(hxs, period_id, 2)
        item['cash_from_financing_activities'] = \
            self.parse_generic(hxs, period_id, 3)
        item['net_change_in_cash'] = \
            self.parse_generic(hxs, period_id, 93)
        item['free_cash_flow'] = \
            self.parse_generic(hxs, period_id, 97)
        return item

    def parse_period_ending(self, hxs, period_id):
        result = hxs.xpath(
            '//div[@id="Year"]/div[@id="%s"]/text()' % period_id).extract()
        return result

    def parse_generic(self, hxs, period_id, data_num):
        result = hxs.xpath(
            '//div[@id="data_i%s"]/div[@id="%s"]/@rawvalue' %
            (data_num, period_id)).extract()
        if len(result) != 0:
            return result
        result = hxs.xpath(
            '//div[@id="data_s%s"]/div[@id="%s"]/@rawvalue' %
            (data_num, period_id)).extract()
        return result
