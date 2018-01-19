# -*- coding: utf-8 -*-
"""
Finds duplicate entries in cointracking.

This script is useful in detecting mistakes eg in manually added deposits/withdrawals.
However, it is quite possible that it reports many duplicate trades that naturally
occur when trading on exchanges.

You can mark a duplicate entry as acceptable by adding `dupok` to the entry's comment.

This script works on a json export as the API has rather low request limits.
"""
import sys
from tools import prettify, read_trades_from_file, convert_trade_objs


if len(sys.argv) != 2:
    print("Usage: {} <json_file>".format(sys.argv[0]))
    exit(1)

all_trades = read_trades_from_file(sys.argv[1])

trade_objs = convert_trade_objs(all_trades)


def list_duplicates(seq):
    seen = set()  # seen values
    dupl = set()  # values listed in duplist
    duplist = []  # result
    for x in seq:
        if x in seen and x not in dupl:
            duplist.append(x)
            dupl.add(x)
        else:
            seen.add(x)
    return duplist

output = []
for d in list_duplicates(trade_objs):
    # Ignore duplicates that have been marked as being ok.
    if 'dupok' not in d.comment:
        output.append(d.to_odict())

if len(output):
    print(prettify(output, indent=4))

print("Checked {} transactions.".format(len(trade_objs)))
print("Found {} duplicates.".format(len(output)))
