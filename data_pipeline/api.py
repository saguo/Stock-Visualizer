from __future__ import absolute_import

import googlefinance

class Api(object):

    @classmethod
    def get_google_finance_quotes(cls, symbol):
        """
        https://pypi.python.org/pypi/googlefinance
        :param symbol: stock symbol, e.g. 'AAPL', or list of stock symbols
        :return: list of dictionary
        """
        return googlefinance.getQuotes(symbol)
