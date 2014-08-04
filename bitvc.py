"""BitVC api features & whatnot"""
import ConfigParser
import requests
import md5
import time
import pprint
from errors import error_text

CFG = ConfigParser.ConfigParser()
CFG.read('config')

def config_map(section):
    """get us some configs"""
    data = {}
    try:
        for name, _ in CFG.items(section):
            try:
                data[name] = CFG.get(section, name)
            except ConfigParser.Error:
                data[name] = None
        return data
    except ConfigParser.NoSectionError:
        return None

def format_check(output):
    """check for errors and print"""
    try:
        msg = error_text(output['code'])
        print "Error {}: {}".format(output['code'], msg)
    except KeyError:
        ppt = pprint.PrettyPrinter(indent=4)
        ppt.pprint(output)

class BitVC(object):
    """make requests, return data, and stuff"""
    def __init__(self):
        self.cfg = config_map('API')

    def sign(self, items):
        """
        computes signed key to pass with authenticated request

        items:  dict of parameters to include in auth request

        returns:    tuple (md5 auth string, timestamp)
        """
        auth = md5.new()
        auth.update("access_key="+self.cfg['key']+"&")

        timestamp = int(time.time())
        items["created"] = timestamp

        for key in sorted(items.iterkeys()):
            auth.update(key+"="+str(items[key])+"&")

        auth.update("secret_key="+self.cfg['secret'])
        return (auth.hexdigest(), timestamp)

    def assets(self):
        """
        get personal assets info

        returns:    dict of balances
        """
        sign = self.sign({})
        params = {'access_key': self.cfg['key'], 'created': sign[1], 'sign': sign[0]}
        req = requests.post(self.cfg['base']+'accountInfo/get', data=params).json()

        return req

    def list_orders(self, currency):
        """
        get list of orders

        currency:   int 2 = Wright (fiat), 1 = BTC

        returns:    list of order dicts
        """
        sign = self.sign({'coin_type': currency})
        params = {'access_key': self.cfg['key'], 'coin_type': currency, 'created': sign[1], 'sign': sign[0]}
        req = requests.post(self.cfg['base']+'order/list', data=params).json()

        return req

    def order_info(self, currency, order_id):
        """
        get info on a specific order

        currency:   int 2 = Wright (fiat), 1 = BTC
        order_id:   int order id

        returns:    dict with order info
        """
        sign = self.sign({'coin_type': currency, 'id': order_id})
        params = {'access_key': self.cfg['key'], 'coin_type': currency, 'created': sign[1], 'sign': sign[0]}
        req = requests.post(self.cfg['base']+'order/'+str(order_id), data=params).json()

        return req

    def order_cancel(self, currency, order_id):
        """
        cancel order

        currency:   int 2 = Wright (fiat), 1 = BTC
        order_id:   int order id

        returns:    dict, check 'Result' key
        """
        sign = self.sign({'coin_type': currency, 'id': order_id})
        params = {'access_key': self.cfg['key'], 'coin_type': currency, 'created': sign[1], 'sign': sign[0]}
        req = requests.post(self.cfg['base']+'cancel/'+str(order_id), data=params).json()

        return req
