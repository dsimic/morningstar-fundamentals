# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IncomeStatementItem(scrapy.Item):
    # define the fields for your item here like:
    symbol = scrapy.Field()
    freq = scrapy.Field()   # ferq is annual or quarterly
    period_ending = scrapy.Field()  # ie: for year / quart ending on
    net_revenue = scrapy.Field()
    net_income = scrapy.Field()
    net_income_available_to_cs = scrapy.Field()
    EBITDA = scrapy.Field()


class BalanceStatementItem(scrapy.Item):
    # define the fields for your item here like:
    symbol = scrapy.Field()
    freq = scrapy.Field()   # ferq is annual or quarterly
    period_ending = scrapy.Field()  # ie: for year / quart ending on
    assets = scrapy.Field()
    liabilities = scrapy.Field()
    stock_holders_equity = scrapy.Field()


class CashFlowItem(scrapy.Item):
    # define the fields for your item here like:
    symbol = scrapy.Field()
    freq = scrapy.Field()   # ferq is annual or quarterly
    period_ending = scrapy.Field()  # ie: for year / quart ending on
    cash_from_operating_activities = scrapy.Field()
    cash_from_investment_activities = scrapy.Field()
    cash_from_financing_activities = scrapy.Field()
    net_change_in_cash = scrapy.Field()
    free_cash_flow = scrapy.Field()
