# Python module for easy integration with uAPI (ucoz API).
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.1 dated April 15, 2020

from urllib.parse import quote_plus, urlencode
from time import time
from sys import maxsize
from random import randint
from hashlib import md5
import hmac
from base64 import b64encode
import requests


class Request(object):

    def __init__(self, site, transfer_protocol, config):
        self.site = site
        self.transfer_protocol = transfer_protocol
        self.config = config
        self.params = {
            'oauth_version': '1.0',
            'oauth_timestamp': int(time()),
            'oauth_nonce': md5(str(str(time()) + str(randint(0, maxsize))).encode('utf-8')).hexdigest(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_consumer_key': self.config['oauth_consumer_key'],
            'oauth_token': self.config['oauth_token']
        }

    def __get_signature(self, method, url, params):
        base_string = method.upper() + '&' + quote_plus(url) + '&' \
                      + quote_plus(Request.__http_build_query(params).replace('+', '%20'))
        return quote_plus(b64encode(Request.__hash_hmac('sha1', base_string, self.config['oauth_consumer_secret'] + '&'
                                                        + self.config['oauth_token_secret'], True)).decode("utf-8"))

    @staticmethod
    def __http_build_query(params):
        return urlencode(dict(sorted(params.items())))

    @staticmethod
    def __hash_hmac(algorithm, data, key, raw_output=False):
        if raw_output:
            res = hmac.new(key.encode(), data.encode(), algorithm).digest()
        else:
            res = hmac.new(key.encode(), data.encode(), algorithm).hexdigest()
        return res

    def get(self, url, data=None):
        self.params['oauth_nonce'] = md5(str(str(time()) + str(randint(0, maxsize))).encode('utf-8')).hexdigest()
        url = self.transfer_protocol + '://' + self.site + '/uapi' + url
        query_string = Request.__http_build_query(dict(self.params, **data, **{
            'oauth_signature': self.__get_signature('get', url, dict(self.params, **data))}))
        request = url + '?' + query_string
        response = requests.get(request).json()
        return response

    def post(self, url, data):
        self.params['oauth_nonce'] = md5(str(str(time()) + str(randint(0, maxsize))).encode('utf-8')).hexdigest()
        url = self.transfer_protocol + '://' + self.site + '/uapi' + url
        response = requests.post(url, data=dict(self.params, **data, **{
            'oauth_signature': self.__get_signature('post', url, dict(self.params, **data))})).json()
        return response

    def put(self, url, data):
        self.params['oauth_nonce'] = md5(str(str(time()) + str(randint(0, maxsize))).encode('utf-8')).hexdigest()
        url = self.transfer_protocol + '://' + self.site + '/uapi' + url
        response = requests.put(url, data=dict(self.params, **data, **{
            'oauth_signature': self.__get_signature('put', url, dict(self.params, **data))})).json()
        return response

    def delete(self, url, data):
        self.params['oauth_nonce'] = md5(str(str(time()) + str(randint(0, maxsize))).encode('utf-8')).hexdigest()
        url = self.transfer_protocol + '://' + self.site + '/uapi' + url
        query_string = Request.__http_build_query(dict(self.params, **data, **{
            'oauth_signature': self.__get_signature('delete', url, dict(self.params, **data))}))
        request = url + '?' + query_string
        response = requests.delete(request).json()
        return response
