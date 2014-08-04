"""BitVC api features & whatnot"""
import ConfigParser
import requests
import md5
import time
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

        returns: json dict of balances
        """
        sign = self.sign({})
        params = {'access_key': self.cfg['key'], 'created': sign[1],
                'sign': sign[0]}
        req = requests.post(self.cfg['base']+'accountInfo/get', data=params)
        return req.json()
