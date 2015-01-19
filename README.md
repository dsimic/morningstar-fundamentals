morningstar
==========

Scrapy spider which can be used to scrape financial statement data from
morningstar.com.

Currently, it scraps very basic cashflow and income statement items.

!!WARNING!!
------
You should not scrape any website that you do not own unless you have gotten
consent from the webmaster of the site. Using these scripts, can and will cause
you to be blacklisted if used abusively and/or incorrectly. This repository is
for reference purposes only and should not be run on a live environment.


Install
-------

To install dependencies:

```sh
pip install -r requirements.txt
```

fundamentals/example has two example scripts of live usage:

```sh
fundamentals/example/run_cashflow_spider.sh
./run_incomestatement_spider.sh
```

This will produce output json files of the scraped pages in fundamentals/example/tmp/.
