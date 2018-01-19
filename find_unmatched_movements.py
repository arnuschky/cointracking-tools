# -*- coding: utf-8 -*-
"""
Finds movement entries (INs/OUTs) that don't have a matching entry in the other direction.
Essentially, this script verify the consistency of double-entry-bookkeeping.
Very useful.

This script works on a json export as the API has rather low request limits.
"""
import sys
from tools import prettify, read_trades_from_file, convert_trade_objs


if len(sys.argv) != 2:
    print("Usage: {} <json_file>".format(sys.argv[0]))
    exit(1)

all_trades = read_trades_from_file(sys.argv[1])

trade_objs = sorted(convert_trade_objs(all_trades))


def do_movements_match(trade1, trade2):
    if trade1.time != trade2.time:
        return False

    # make sure there is a withdrawal
    if 'Withdrawal' == trade1.type:
        withdrawal = trade1
    elif 'Withdrawal' == trade2.type:
        withdrawal = trade2
    else:
        return False

    # make sure there is a deposit
    if 'Deposit' == trade1.type:
        deposit = trade1
    elif 'Deposit' == trade2.type:
        deposit = trade2
    else:
        return False

    if withdrawal.sell_currency != deposit.buy_currency:
        return False

    # totals match
    if withdrawal.sell_amount - withdrawal.fee_amount != deposit.buy_amount + deposit.fee_amount:
        return False

    return True

num_unmatched = 0

for i in range(0, len(trade_objs)):
    trade = trade_objs[i]
    
    if trade.type != 'Withdrawal' and trade.type != 'Deposit':
        continue

    finds = [trade]

    # step backwards
    j = i - 1
    while j >= 0 and trade_objs[j].time == trade.time:
        if do_movements_match(trade_objs[j], trade):
            finds.append(trade_objs[j])
        j -= 1

    # step forwards
    j = i + 1
    while j < len(trade_objs) and trade_objs[j].time == trade.time:
        if do_movements_match(trade_objs[j], trade):
            finds.append(trade_objs[j])
        j += 1

    if len(finds) == 1:
        print("Found no match for the following movement:")
        print(prettify(finds[0].to_odict()))
        num_unmatched += 1

    if len(finds) > 2:
        print("Found too many matches for the movement.")
        print("Check for duplicates!")
        # for found in finds:
        #     print(prettify(found.to_odict()))
        # num_unmatched += 1

print("Checked {} transactions.".format(len(trade_objs)))
print("Found {} unmatched movements.".format(num_unmatched))
