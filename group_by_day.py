# -*- coding: utf-8 -*-
"""

This script groups trades that occur on the same day. To allow grouping, ecords must have:

 - the same currency pair
 - the same exchange
 - the same date

The script does NOT work on the API but processes a csv file. This is useful for
reporting margin trades as described here: https://cointracking.freshdesk.com/en/support/solutions/articles/29000018275-margin-trades-profit-determination

Expected csv input format (set this up by selecting the right columns in the "Trade List"):

     Buy amount, Buy currency, Buy in EUR, Sell amount, Sell currency, Sell in EUR, Exchange, Date

For example:

    1.95852928, BTC, 114.87092795, 1312.95150627, XMR, 116.15735953, Poloniex, 30.08.2016 13:31

Output format is the same.
"""
import csv
import sys

from decimal import Decimal


class Record(object):

    def __init__(self, buyamt, buycur, buyeur, sellamt, sellcur, selleur, exchange, date):
        self.buyamt = Decimal(buyamt)
        self.buycur = buycur
        self.buyeur = Decimal(buyeur)
        self.sellamt = Decimal(sellamt)
        self.sellcur = sellcur
        self.selleur = Decimal(selleur)
        self.exchange = exchange
        self.date = date.strip().split(' ')[0]

    def __str__(self):
        """
        Exports as csv row.
        """
        return "{},{},{},{},{},{},{},{}".format(self.buyamt, self.buycur, self.buyeur, self.sellamt,
                                                self.sellcur, self.selleur, self.exchange, self.date)

    def __eq__(self, other):
        """
        Returns True if two records can be combined (same currencies, same venue, same date)
        """
        res = self.buycur == other.buycur and self.sellcur == other.sellcur and \
            self.exchange == other.exchange and self.date == other.date
        return res

    def __add__(self, other):
        """
        Adds two records by adding amounts only.
        """
        return Record(self.buyamt + other.buyamt, self.buycur, self.buyeur + other.buyeur,
                      self.sellamt + other.sellamt, self.sellcur, self.selleur + other.selleur,
                      self.exchange, self.date)


if len(sys.argv) != 3:
    print("Usage: {} <csv_in> <csv_out>".format(sys.argv[0]))
    exit(1)


output = []
previous = None
header = None

with open(sys.argv[1]) as csvfile:
    csvdata = csv.reader(csvfile, delimiter=',', )

    for row in csvdata:
        if header is None:
            # keep header for output
            header = row
            continue

        record = Record(*row)
        if previous is None:
            # first row, set as previous
            previous = record
            continue

        if record == previous:
            # new row can be combined with previous
            previous += record
            continue

        else:
            # can't be combined, adding previous to output then switch over
            output.append(previous)
            previous = record

    output.append(previous)

if output:
    with open(sys.argv[2], 'w') as csvfile:
        print(header)
        csvfile.writelines(','.join(header) + '\n')
        for record in output:
            csvfile.write(str(record) + '\n')

print("Exported {} records.".format(len(output)))
