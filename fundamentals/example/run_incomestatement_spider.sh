#!/bin/bash 

SPIDER="incomestatement"; OUTFILE="tmp/${SPIDER}.json";  rm -f $OUTFILE; \
    scrapy crawl $SPIDER -o $OUTFILE --set SYMBOL_FILE=symbols.csv
