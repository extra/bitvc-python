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
        self.cfg = config_map('api')

    def sign(self, items):
        """
        computes signed key to pass with authenticated request

        items:  dict of parameters to include in auth request

        returns:    md5 auth string
        """
        auth = md5.new()
        auth.update("access_key="+self.cfg['key'])
        items["created"] = int(time.time())

        for key in sorted(items.iterkeys()):
            auth.update(key+"="+items[key])

        auth.update("secret_key="+self.cfg['secret'])
