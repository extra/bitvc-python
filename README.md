BitVC Python Libs
=================

###Setup

Run `git clone https://github.com/extra/bitvc-python.git`

###Config

Specify required settings in `config`

```
api = https://api.bitvc.com/api/

key = abcd-123-456
secret = defg-999-8888
```

###Usage

Until some clients are built out, just call methods directly. Currently you can use:

--- `sign(items)` --> compute md5 for request (internal, you probvably don't need this).
--- `assets()` --> get personal assets info.
--- `list_orders(currency)` --> list orders for specified currency (1 = BTC, 2 = fiat).
--- `order_info(currency, order_id)` --> get info about a specific order.
--- `order_cancel(currency, order_id)` --> cancel an order.

```
>>> from bitvc import BitVC
>>> b = BitVC()
>>> b.assets()
{   u'available_btc': u'123.0000',
    u'available_cny': u'1000.00',
    u'available_ltc': u'123.0000',
    u'frozen_btc': u'0.0000',
    u'frozen_cny': u'0.00',
    u'frozen_ltc': u'0.0000',
    u'loan_btc': u'0.0000',
    u'loan_cny': u'0.00',
    u'loan_ltc': u'0.0000'}
```
