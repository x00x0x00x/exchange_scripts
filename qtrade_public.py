import requests
import ast
import json
import matplotlib.pyplot as plt

api_methods = ['ticker', 'tickers', 'currency', 'currencies', 'common', 'market', 'markets', 'orderbook', ]

class Req:
    def __init__(self, api_method, args=None, api_version='v1'):
        self.res = None
        if args is None:
            args = []

        self.base_url = 'https://api.qtrade.io/'+api_version+'/'+api_method
        if len(args) > 0:
            for arg in args:
                self.base_url += '/'+arg

    def make_request(self):
        temp_res = requests.get(self.base_url)
        print(temp_res.content.decode('utf-8'))
        if temp_res.status_code == 200:
            self.res = json.loads(temp_res.content.decode('utf-8'))
        return self.res

## public start

class Ticker:
    def __init__(self, market_string):
        self.market_string = market_string

    def make_request(self):
        return Req('ticker', args=[self.market_string]).make_request()

class Tickers:
    def __init__(self):
        self.name = 'tickers'

    def make_request(self):
        return Req(self.name).make_request()

class Currency:
    def __init__(self, currency_ticker):
        self.currency_ticker = currency_ticker

    def make_request(self):
        return Req('currency', args=[self.currency_ticker]).make_request()

class Currencies:
    def make_request(self):
        return Req('currencies').make_request()

class Common:
    def make_request(self):
        return Req('common').make_request()

class Market:
    def __init__(self, market_string):
        self.market_string = market_string

    def make_request(self):
        return Req('market', args=[self.market_string])

class Markets:
    def make_request(self):
        return Req('markets').make_request()

class Trades:
    def __init__(self, market_string):
        self.market_string = market_string

    def make_request(self):
        return Req('market', args=[self.market_string, 'trades']).make_request()

class Orderbook:
    def __init__(self, market_string):
        self.market_string = market_string

    def make_request(self):
        return Req('orderbook', args=[self.market_string]).make_request()

ohlcv_ts_slices = ['fivemin', 'fifteenmin', 'thirtymin', 'onehour', 'twohour', 'fourhour', 'oneday']

class OHLCV:
    def __init__(self, market_string, time_scale_interval):
        self.market_string = market_string
        if time_scale_interval in ohlcv_ts_slices:
            self.time_scale_interval = time_scale_interval

    def make_request(self):
        return Req('market', args=[self.market_string, 'ohlcv', self.time_scale_interval]).make_request()

## public end

class Plot:  # amt_lines=Int, title=Str, x,y=List or List[List], x,y_label=Str, line_label=Str or List
    def __init__(self, amt_lines=1, title='', x=None, y=None, x_label='', y_label='', line_label=''):
        self.amt_lines = amt_lines
        self.x_label = x_label
        self.y_label = y_label
        if x is None and y is None:
            exit('x and y arguments for Plot object missing')

        if amt_lines is not int:
            exit('amt_lines is not an integer')

        if amt_lines == 1:
            self.lines = [{
                'x': x,
                'y': y,
                'line_label': line_label,
                'title': title
            }]
        elif amt_lines > 1:
            self.lines = []

            self.xs = x
            self.ys = y
            self.titles = title
            self.x_label = x_label
            self.y_label = y_label
            self.line_labels = line_label

            if type(x[0]) == list and type(y[0]) == list and type(line_label) == list:
                arg_lens = [self.amt_lines, len(x), len(y), len(line_label)]
                if len(set(arg_lens)) > 1:
                    exit('Wrong amount of arguments supplied. All variable lists should be equal in length to amt_lines. Title, x_label, y_label = str')

                for i in range(amt_lines):
                    self.lines.append({
                        'x': self.xs[i],
                        'y': self.ys[i],
                        'line_label': self.line_labels[i],
                        'title': title
                    })


    def make_plot(self):
        if self.amt_lines == 1:
            plot_config = self.lines[0]
            plt.plot(plot_config['x'], plot_config['y'], label=plot_config['line_label'])
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
        elif self.amt_lines > 1:
            for i in range(self.amt_lines):
                plot_config = self.lines[i]
                plt.plot(plot_config['x'], plot_config['y'], label=plot_config['line_label'])
                plt.xlabel(self.x_label)
                plt.ylabel(self.y_label)
        else:
            exit('Failed to make plot')

        plt.legend()
        plt.show()


tickers = Tickers()
tickers = tickers.make_request()

ticker = Ticker('NYZO_BTC')
ticker = ticker.make_request()

currencies = Currencies()
currencies = currencies.make_request()

currency = Currency('BTC')
currency = currency.make_request()

common = Common()
common = common.make_request()

market = Market('NYZO_BTC')
market = market.make_request()

markets = Markets()
markets = markets.make_request()

trades = Trades('NYZO_BTC')
trades = trades.make_request()

orderbook = Orderbook('NYZO_BTC')
orderbook = orderbook.make_request()

ohlcv = OHLCV('NYZO_BTC', 'oneday')
ohlcv = ohlcv.make_request()

print(tickers)
print(ticker)
print(currencies)
print(currency)
print(common)
print(market)
print(markets)
print(trades)
print(orderbook)
print(ohlcv)
