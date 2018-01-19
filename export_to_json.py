# -*- coding: utf-8 -*-
"""
Simple script that exports all trades from cointracking and write them into a json file.

Note that the exported json is NOT compatible with the json export from the cointracking site.
"""
import json
import sys

from api import get_trades


if len(sys.argv) != 2:
    print("Usage: {} <json_file>".format(sys.argv[0]))
    exit(1)

all_trades = get_trades()

with open(sys.argv[1], 'w') as output_file:
    json.dump(all_trades, output_file, indent=4)

print("Success. Exported {} items.".format(len(all_trades)))
