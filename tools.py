# -*- coding: utf-8 -*-
"""
Some tools useful in conjunction with the API, for example a Trade object.
"""
import json
from collections import OrderedDict
from datetime import datetime, date
from decimal import Decimal

try:
    # noinspection PyUnresolvedReferences
    from pygments import highlight, lexers, formatters
    pygments_available = True
except ImportError:
    pygments_available = False


def prettify(data, use_colors=pygments_available, indent=4, newlines=True):
    """
    Prints a dict as prettily formatted json (with indents).
    Uses colors if available.
    @param data: Data to print as json.
    @type data: dict|list
    @param use_colors: If true, use colors. Default is True if pygments is installed.
    @type use_colors: bool
    @param indent: Number of spaces to indent.
    @type indent: int
    @param newlines: Use newlines if True.
    @type newlines: bool
    @return: formatted output
    @rtype: str
    """
    json_str = json.dumps(data, indent=indent, cls=ExtendedJSONEncoder)
    if not newlines:
        json_str = json_str.replace('\n', '')
    if use_colors and pygments_available:
        # noinspection PyUnresolvedReferences
        json_str = highlight(json_str.encode('utf8'),
                             lexers.JsonLexer(), formatters.TerminalFormatter())
    return json_str


def read_trades_from_file(filename):
    """
    Reads trades from a json file.
    :param filename: Filename
    :type filename: str
    :return: trades
    :rtype: dict
    """
    return json.load(open(filename), object_pairs_hook=OrderedDict)


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        return super(ExtendedJSONEncoder, self).default(obj)


class Trade(object):
    """
    A trade object represents a single trade entry in cointracking's API.
    The object allows for hashing, sorting, comparing and the like.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type, time, trade_id, buy_currency, sell_currency, fee_currency,
                 buy_amount, sell_amount, fee_amount, exchange, group, comment, imported_from, imported_time):
        self.type = type.strip()
        self.time = datetime.fromtimestamp(int(time.strip()))
        self.trade_id = trade_id.strip()
        self.buy_currency = buy_currency.strip()
        self.sell_currency = sell_currency.strip()
        self.fee_currency = fee_currency.strip()
        self.buy_amount = Decimal(buy_amount.strip() or 0)
        self.sell_amount = Decimal(sell_amount.strip() or 0)
        self.fee_amount = Decimal(fee_amount.strip() or 0)
        self.exchange = exchange.strip()
        self.group = group.strip()
        self.comment = comment.strip()
        self.imported_from = imported_from.strip()
        self.imported_time = datetime.fromtimestamp(int(imported_time.strip()))

    def __key(self):
        """
        We key data only by the relevant fields. Trade entries might be same but differ in non-relevant fields
        such as comment.
        :return: key
        """
        return (
            self.trade_id, self.type, self.time,
            self.buy_currency, self.sell_currency, self.fee_currency,
            self.buy_amount, self.sell_amount, self.fee_amount
        )

    def __eq__(self, y):
        return self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return str(self.__key())

    def __str__(self):
        return json.dumps(self.to_odict(), cls=ExtendedJSONEncoder)

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def to_odict(self):
        """
        Returns trade data as an ordered dict. Used for dumping object attrs to string in order.
        :return:
        :rtype:
        """
        return OrderedDict([
            ('type', self.type),
            ('time', self.time),
            ('trade_id', self.trade_id),
            ('buy_currency', self.buy_currency),
            ('sell_currency', self.sell_currency),
            ('fee_currency', self.fee_currency),
            ('buy_amount', self.buy_amount),
            ('sell_amount', self.sell_amount),
            ('fee_amount', self.fee_amount),
            ('exchange', self.exchange),
            ('group', self.group),
            ('comment', self.comment),
            ('imported_from', self.imported_from),
            ('imported_time', self.imported_time),
        ])


def convert_trade_objs(trades):
    """
    Converts trade dicts to Trade objects.
    :param trades: Trades as exported by cointracking.
    :type trades: dict
    :return: Ordered list of objects.
    :rtype: list<Trade>
    """
    trade_objs = []
    for trade in trades.values():
        # Strip API returns fields that are not trades (grrrr)
        if trade == 1 or trade == 'getTrades':
            continue

        # Create trade object. Handle exceptions which mean that we hit an unexpected record.
        try:
            trade_objs.append(Trade(**trade))
        except Exception as e:
            print("Exception: {} for trade {}".format(str(e), str(trade)))
            print("Unexpected data? Skipping record.")

    return trade_objs