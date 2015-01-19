# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from fundamentals.mstar_util import get_requests, MSTAR_PERIOD_IDS, get_symbols
from fundamentals.items import IncomeStatementItem
import json


class IncomestatementSpider(scrapy.Spider):
    name = "incomestatement"
    allowed_domains = ["morningstar.com"]

    def __init__(self, settings):
        self.my_settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def start_requests(self):
        report_type = 'is'
        symbols = get_symbols(self.my_settings['SYMBOL_FILE'])
        requests = get_requests(self.parse, symbols, "A", report_type)
        requests += get_requests(self.parse, symbols, "Q", report_type)
        return requests

    def parse(self, response):
        response = response.replace(
            body=json.loads(response.body)['result'])
        print '----reposnse body-----', response.body[0:200]
        hxs = Selector(response)
        for period_id in MSTAR_PERIOD_IDS:
            yield self.parse_period(hxs, period_id, response.meta)

    def parse_period(self, hxs, period_id, meta):
        item = IncomeStatementItem()
        item['symbol'] = meta['symbol']
        item['freq'] = meta['freq']
        item['period_ending'] = self.parse_period_ending(hxs, period_id)
        item['net_revenue'] = self.parse_revenue(hxs, period_id)
        item['net_income'] = self.parse_net_income(hxs, period_id)
        item['net_income_available_to_cs'] = \
            self.parse_net_income_available_to_cs(hxs, period_id)
        item['EBITDA'] = self.parse_EBIDTA(hxs, period_id)
        return item

    def parse_period_ending(self, hxs, period_id):
        result = hxs.xpath(
            '//div[@id="Year"]/div[@id="%s"]/text()' % period_id).extract()
        print "--result--", result
        return result

    def parse_revenue(self, hxs, period_id):
        result = hxs.xpath(
            '//div[@id="data_i1"]/div[@id="%s"]/@rawvalue' % period_id).\
            extract()
        if len(result) != 0:
            return result
        result = hxs.xpath(
            '//div[@id="data_s1"]/div[@id="%s"]/@rawvalue' % period_id).\
            extract()
        return result

    def parse_net_income(self, hxs, period_id):
        result = hxs.xpath(
            '//div[@id="data_i70"]/div[@id="%s"]/@rawvalue' % period_id).\
            extract()
        return result

    def parse_net_income_available_to_cs(self, hxs, period_id):
        row = hxs.xpath('//div[@id="data_i82"]')
        return row.select('div[@id="%s"]/@rawvalue' % period_id).extract()

    def parse_EBIDTA(self, hxs, period_id):
        row = hxs.xpath('//div[@id="data_i90"]')
        return row.select('div[@id="%s"]/@rawvalue' % period_id).extract()
