# -*- coding: utf-8 -*-
"""
Simple testscript that pulls all data from the API and pretty-prints it.
"""
from api import *
from tools import prettify


print('#' * 120)
print(prettify(get_trades()))

print('#' * 120)
print(prettify(get_balance()))

# print('#' * 120)
# print(prettify(get_historical_summary()))
#
# print('#' * 120)
# print(prettify(get_historical_currency()))

print('#' * 120)
print(prettify(get_grouped_balance()))

print('#' * 120)
print(prettify(get_gains()))
