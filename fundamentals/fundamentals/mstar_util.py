import scrapy

url = 'http://financials.morningstar.com/ajax/ReportProcess4HtmlAjax.html'

MSTAR_PERIOD_IDS = ["Y_1", "Y_2", "Y_3", "Y_4", "Y_5"]

MSTAR_SYMBOLS = ["XNYS:C", "XNYS:IBM", "XNAS:GOOG"]

FREQ_MAP = {
    'A': 12,
    'Q': 3,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0)' +
    ' Gecko/20100101 Firefox/28.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_symbols(symbols_file):
    if symbols_file is not None:
        import csv
        with open(symbols_file, 'rb') as f:
            reader = csv.reader(f)
            symbols = [row[0] for row in list(reader)]
    else:
        symbols = MSTAR_SYMBOLS
    print "symbols--------", symbols
    return symbols


def get_data(symbol, freq, report_type):
    return {
        't': symbol,
        'columnYear': 5,
        'dataType': 'A',
        'period': FREQ_MAP[freq],
        'reportType': report_type,
    }


def get_url(symbol, freq, report_type, url=url):
    url += "?"
    for key, value in get_data(symbol, freq, report_type).items():
        url += "&%s=%s" % (key, value)
    return url


def get_requests(callback, symbols, freq, report_type):
    return [
        scrapy.Request(
            get_url(symbol, freq, report_type),
            callback,
            meta={
                "symbol": symbol,
                "freq": freq},
            headers=headers)
        for symbol in symbols
    ]


