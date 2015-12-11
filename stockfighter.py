import requests, json
from ws4py.client.threadedclient import WebSocketClient
from ws4py.messaging import TextMessage

class Stockfighter:
    API_KEY = open('api', 'r').read().strip()

    def __init__(self, venue, account):
        self.venue = venue
        self.account = account
        
    def heartbeat(self):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.HEARTBEAT)
        return True

    def check_venue(self):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.VENUE % { 'venue': self.venue })
        return True

    def list_stocks(self):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.STOCKS % { 'venue': self.venue })
        return response['symbols']

    def orderbook(self, stock):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.ORDERBOOK % { 'venue': self.venue, 'stock': stock })
        return response

    def order(self, stock, price, qty, direction, orderType, raw=True):
        data = {
                'account': self.account,
                'venue': self.venue,
                'stock': stock,
                'price': price,
                'qty': qty,
                'direction': direction,
                'orderType': orderType
                }
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.ORDER % { 'venue': self.venue, 'stock': stock }, data, raw)
        return response

    def quote(self, stock):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.QUOTE % { 'venue': self.venue, 'stock': stock })
        return response

    def order_status(self, stock, order):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.ORDER_STATUS % { 'venue': self.venue, 'stock': stock, 'id': str(order) })
        return response

    def cancel(self, stock, order):
        #response, status_code = Stockfighter.Web.delete(Stockfighter.Web.URLS.CANCEL % { 'venue': self.venue, 'stock': stock, 'order': order })
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.CANCEL % { 'venue': self.venue, 'stock': stock, 'id': str(order) })
        return response

    def my_orders(self):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.MY_ORDERS % { 'venue': self.venue, 'account': self.account })
        return response

    def quote_venue_ticker(self, callback):
        def wrapper(msg):
            if isinstance(msg, TextMessage):
                msg = json.loads(msg.data)
            if msg is None:
                callback(None)
            else:
                callback(msg['quote'])
        Stockfighter.Web.WebSocketClient(Stockfighter.Web.URLS.VENUE_TICKER % { 'account': self.account, 'venue': self.venue }, wrapper)

    def quote_stock_ticker(self, callback, stock):
        def wrapper(msg):
            if isinstance(msg, TextMessage):
                msg = json.loads(msg.data)
            if msg is None:
                callback(None)
            else:
                callback(msg['quote'])
        Stockfighter.Web.WebSocketClient(Stockfighter.Web.URLS.STOCK_TICKER % { 'account': self.account, 'venue': self.venue, 'stock': stock }, wrapper)

    def execution_venue_ticker(self, callback):
        def wrapper(msg):
            if isinstance(msg, TextMessage):
                msg = json.loads(msg.data)
            if msg is None:
                callback(None)
            else:
                callback(msg)
        Stockfighter.Web.WebSocketClient(Stockfighter.Web.URLS.EXECUTIONS_VENUE_TICKER % { 'account': self.account, 'venue': self.venue }, wrapper)

    def execution_stock_ticker(self, callback, stock):
        def wrapper(msg):
            if isinstance(msg, TextMessage):
                msg = json.loads(msg.data)
            if msg is None:
                callback(None)
            else:
                callback(msg)
        Stockfighter.Web.WebSocketClient(Stockfighter.Web.URLS.EXECUTIONS_STOCK_TICKER % { 'account': self.account, 'venue': self.venue, 'stock': stock }, wrapper)

    @staticmethod
    def get_levels():
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.GET_LEVELS)
        return response

    @staticmethod
    def start_level(name):
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.START_LEVEL % { 'name': name })
        return response

    @staticmethod
    def resume_level(_id):
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.RESUME_LEVEL % { 'id': _id })
        return response

    @staticmethod
    def restart_level(_id):
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.RESTART_LEVEL % { 'id': _id })
        return response

    @staticmethod
    def stop_level(_id):
        response, status_code = Stockfighter.Web.post(Stockfighter.Web.URLS.STOP_LEVEL % { 'id': _id })
        return response

    @staticmethod
    def check_level(_id):
        response, status_code = Stockfighter.Web.get(Stockfighter.Web.URLS.LEVEL_INFO % { 'id': _id })
        return response

    class Web:
        class URLS:
            GET_LEVELS =    'https://www.stockfighter.io/ui/levels'
            START_LEVEL =   'https://www.stockfighter.io/gm/levels/%(name)s'
            RESUME_LEVEL =  'https://www.stockfighter.io/gm/instances/%(id)s/resume'
            RESTART_LEVEL = 'https://www.stockfighter.io/gm/instances/%(id)s/restart'
            STOP_LEVEL =    'https://www.stockfighter.io/gm/instances/%(id)s/stop'
            LEVEL_INFO =    'https://www.stockfighter.io/gm/instances/%(id)s'

            HEARTBEAT =     'https://api.stockfighter.io/ob/api/heartbeat'
            VENUE =         'https://api.stockfighter.io/ob/api/venues/%(venue)s/heartbeat'
            STOCKS =        'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks'
            ORDERBOOK =     'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s'
            ORDER =         'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s/orders'
            QUOTE =         'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s/quote'
            ORDER_STATUS =  'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s/orders/%(id)s'
            #CANCEL =        'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s/orders/%(order)s'
            CANCEL =        'https://api.stockfighter.io/ob/api/venues/%(venue)s/stocks/%(stock)s/orders/%(id)s/cancel'
            MY_ORDERS =     'https://api.stockfighter.io/ob/api/venues/%(venue)s/accounts/%(account)s/orders'
            
            VENUE_TICKER =  'wss://api.stockfighter.io/ob/api/ws/%(account)s/venues/%(venue)s/tickertape'
            STOCK_TICKER =  'wss://api.stockfighter.io/ob/api/ws/%(account)s/venues/%(venue)s/tickertape/stocks/%(stock)s'

            EXECUTIONS_VENUE_TICKER = 'wss://api.stockfighter.io/ob/api/ws/%(account)s/venues/%(venue)s/executions'
            EXECUTIONS_STOCK_TICKER = 'wss://api.stockfighter.io/ob/api/ws/%(account)s/venues/%(venue)s/executions/stocks/%(stock)s'

        @staticmethod
        def get(url):
            return Stockfighter.Web.process(Stockfighter.Web._get(url))

        @staticmethod
        def _get(url):
            headers = { 'X-Starfighter-Authorization': Stockfighter.API_KEY }
            r = requests.get(url, headers=headers)
            response = r.json() # Let the exception go through if json fails
            return response, r.status_code

        @staticmethod
        def post(url, data={}, raw=False):
            if raw: data = json.dumps(data)
            return Stockfighter.Web.process(Stockfighter.Web._post(url, data))

        @staticmethod
        def _post(url, data):
            headers = { 'X-Starfighter-Authorization': Stockfighter.API_KEY }
            r = requests.post(url, headers=headers, data=data)
            response = r.json() # Let the exception go through if json fails
            return response, r.status_code

        @staticmethod
        def delete(url):
            return Stockfighter.Web.process(Stockfighter.Web._delete(url))

        @staticmethod
        def _delete(url):
            headers = { 'X-Starfighter-Authorization': Stockfighter.API_KEY }
            r = requests.post(url, headers=headers)
            print r.text
            response = r.json() # Let the exception go through if json fails
            return response, r.status_code

        @staticmethod
        def process(data):
            response, response_code = data
            if response:
                if response['ok']:
                    return response, response_code
                raise Stockfighter.Exception(response_code, response['error'])
            raise Stockfighter.Exception(-1, 'Uh oh')

        class WebSocketClient(WebSocketClient):
            def __init__(self, url, msg_callback):
                WebSocketClient.__init__(self, url)
                self.callback = msg_callback
                self.connect()

            def opened(self):
                print 'Web socket opened!'

            def closed(self, code, reason=None):
                print 'Web socket closed!'
                self.callback(None)

            def received_message(self, msg):
                msg = json.loads(msg.data)
                self.callback(msg)
    
    class Exception(Exception):
        def __init__(self, status_code=-1, error=''):
            self.status_code = status_code
            self.error = error
            Exception.__init__(self, '%i: %s' % (status_code, error))
