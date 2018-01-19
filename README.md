# cointracking-tools

Python API and tools for cointracking.info

This repository contains a few scripts that helped me manage my cryptocurrency-related data on cointracking.info. 

At the time of writing these scripts (end of 2017), cointracking had some severe flaws and deficiencies that made it nearly impossible for me to complete my tax return. Luckily it offers an API so that I could write some helpers to wrangle the data a bit better.

This is pretty hacked up and definitely not tested beyond my own personal use. Hope this is useful for someone.

## Requirements

Tested with Python 3.5. See `requirements.txt` for dependencies. Use a virtualenv.

## General API wrapper

### `api.py`

This is a very simple wrapper for the cointracking.info API.
Basically only does marshalling etc.

Usage:
 1. Set `API_KEY` and `API_SECRET` environment variables
 2. `import api`
 3. call methods, eg `api.get_trades()`

### `tools.py`

Some tools useful in conjunction with the API, for example a Trade object.

## Scripts

## `display_data.py`

Simple testscript that pulls all data from the API and pretty-prints it.

## `export_to_json.py`

Simple script that exports all trades from cointracking and write them into a json file.

Note that the exported json is NOT compatible with the json export from the cointracking site.

## `find_duplicates.py`

Finds duplicate entries in cointracking.

This script is useful in detecting mistakes eg in manually added deposits/withdrawals.
However, it is quite possible that it reports many duplicate trades that naturally
occur when trading on exchanges.

You can mark a duplicate entry as acceptable by adding `dupok` to the entry's comment.

This script works on a json export as the API has rather low request limits.

## `find_unmatched_movements.py`

Finds movement entries (INs/OUTs) that don't have a matching entry in the other direction.
Essentially, this script verify the consistency of double-entry-bookkeeping.
Very useful.

This script works on a json export as the API has rather low request limits.

## `group_by_day.py`

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