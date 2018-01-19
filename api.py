# -*- coding: utf-8 -*-
"""
This is a very simple wrapper for the cointracking.info API.
Basically only does marshalling etc.

Usage:
 1. Set `API_KEY` and `API_SECRET` environment variables
 2. `import api`
 3. call methods, eg `api.get_trades()`
"""
import os
import time
import logging
import hashlib
import hmac
import urllib.parse

import requests


log = logging.getLogger(__name__)

API_URL = 'https://cointracking.info/api/v1/'

API_KEY = os.environ['COINTRACKING_API_KEY']
API_SECRET = os.environ['COINTRACKING_API_SECRET'].encode('utf-8')


def _api_call(api_method, **kwargs):
    payload = {}

    # Copy over any argument that's none None (None would use API default).
    for key in kwargs.keys():
        if kwargs[key] is not None:
            payload[key] = kwargs[key]

    payload['method'] = api_method
    payload['nonce'] = int(time.time() * 1000)

    payload_bytes = urllib.parse.urlencode(payload).encode('utf8')
    signed_payload = hmac.new(API_SECRET, payload_bytes, hashlib.sha512).hexdigest()

    headers = {
        'Key': API_KEY,
        'Sign': signed_payload,
    }

    r = requests.post(API_URL, headers=headers, data=payload)
    return r.json()


def get_trades(limit=None, order=None, start_time=None, end_time=None):
    """
    Returns all your CoinTracking trades and transactions.
    Similar to the 'Trade List' on the website.
    @param limit: Number of trades. `None` will use API default (all).
    @type limit: int
    @param order: Trade ordering. `None` will use API default (by time, ascending).
    @type order: str
    @param start_time: Only list trades after this time. `None` will use API default (no start time).
    @type start_time: int
    @param end_time: Only list trades before this time.`None` will use API default (no end time).
    @type end_time: int
    @return: result as dict
    @rtype: dict
    """
    return _api_call('getTrades', limit=limit, order=order, start_time=start_time, end_time=end_time)


def get_balance():
    """
    Returns your current CoinTracking account and coin balance.
    Similar to the `Current Balance` on the website.
    @return: result as dict
    @rtype: dict
    """
    return _api_call('getBalance')


def get_historical_summary(show_as_btc=None, start_time=None, end_time=None):
    """
    Returns all historical values for all your coins, currencies, commodities, and the total account value.
    Similar to the `Daily Balance` or the `Trade Statistics` on the website.
    @param show_as_btc: True to show values in BTC, False to show values in fiat currency. `None` will use API default.
    @type show_as_btc: bool
    @param start_time: Only list trades after this time. `None` will use API default (no start time).
    @type start_time: int
    @param end_time: Only list trades before this time.`None` will use API default (no end time).
    @type end_time: int
    @return: result as dict
    @rtype: dict
    """
    btc = 1 if show_as_btc else 0
    return _api_call('getHistoricalSummary', btc=btc, start_time=start_time, end_time=end_time)


def get_historical_currency(currency=None, start_time=None, end_time=None):
    """
    Returns all historical amounts and values for a specific currency/coin or for all currencies/coins.
    Similar to the `Daily Balance` or the `Trade Statistics` on the website.
    @param currency: Load only values of this currency/coin (e.g. ETH). `None` will use API default (load historical
                     values for all currencies/coins).
    @type currency: str
    @param start_time: Only list trades after this time. `None` will use API default (no start time).
    @type start_time: int
    @param end_time: Only list trades before this time.`None` will use API default (no end time).
    @type end_time: int
    @return: result as dict
    @rtype: dict
    """
    return _api_call('getHistoricalCurrency', currency=currency, start_time=start_time, end_time=end_time)


# noinspection PyShadowingBuiltins
def get_grouped_balance(group=None, exclude_movements=None, type=None):
    """
    Returns the current balance grouped by exchange, trade-group or transaction type.
    Similar to the `Balance by Exchange` on the website.
    @param group: Field to group by, either `exchange`, `group` or `type`. `None` will use API default (exchange).
    @type group: str
    @param exclude_movements: Set to True to exclude account movements (deposits/withdrawals). Excluding
                              movements is recommended. `None` will use API default (True).
    @type exclude_movements: bool
    @param type: `None` to calculate all transaction types. Set a type to calculate the balance for a specific type.
                 Possible types: `Trade`, `Deposit`, `Withdrawal`, `Income`, `Mining`, `Gift/Tip(In)`,
                                 `Spend`, `Donation`, `Gift(Out)`, `Stolen`, `Lost`
    @type type: str
    @return: result as dict
    @rtype: dict
    """
    exclude_dep_with = 1 if exclude_movements else 0
    return _api_call('getGroupedBalance', group=group, exclude_dep_with=exclude_dep_with, type=type)


def get_gains(method=None, price=None, exclude_movements=None, cost_basis=None, show_as_btc=None):
    """
    Returns your current realized and unrealized gains data.
    Similar to the `Realized and Unrealized Gains` on the website.
    Setting parameters to `None` will use API defaults, which depends on your account setting.
    @param method: Possible methods: FIFO, LIFO, HIFO, LOFO, HPFO, LPFO, HAFO, LAFO.
    @type method: str
    @param price: Possible values: best, transaction, counterpart
    @type price: str
    @param exclude_movements: Set to True to exclude account movements (deposits/withdrawals). Excluding
                              movements is recommended. `None` will use API default (True).
    @type exclude_movements: bool
    @param cost_basis: Possible values: unsold (recommended) and all
    @type cost_basis: str
    @param show_as_btc: True to show values in BTC, False to show values in fiat currency. `None` will use API default.
    @type show_as_btc: bool
    @return: result as dict
    @rtype: dict
    """
    exclude_dep_with = 1 if exclude_movements else 0
    btc = 1 if show_as_btc else 0
    return _api_call('getGains', method=method, price=price, exclude_dep_with=exclude_dep_with,
                     costbasis=cost_basis, btc=btc)
