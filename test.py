from stockfighter import Stockfighter

fighter = Stockfighter('TESTEX', 'EXB123456')
stock = 'FOOBAR'

if fighter.heartbeat(): print 'API is up!'

try:
    print 'Testing venue...',
    fighter.check_venue()
    print '%s venue is up!' % fighter.venue
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing stock listing...',
    symbols = fighter.list_stocks()
    print 'Stocks available at %s:' % fighter.venue,symbols
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing orderbook...',
    orderbook = fighter.orderbook(stock)
    print '\n\t Orderbook bids:',orderbook['bids'],'\n\t Orderbook asks:',orderbook['asks']
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing websocket tickers'

    def quote_ticker(quote):
        if quote is None:
            fighter.quote_stock_ticker(quote_ticker, stock) # This will auto-restart the ticker if it dies
            return

        print '\t --- Quote from ticker: %s... ---\n' % str(quote)[:40],

    def execution_ticker(execution):
        if execution is None:
            fighter.execution_stock_ticker(execution_ticker, stock) # This will auto-restart the ticker if it dies
            return

        print '\t --- Execution from ticker: %s... ---\n' % str(execution)[:40],

    fighter.quote_stock_ticker(quote_ticker, stock)
    fighter.execution_stock_ticker(execution_ticker, stock)

except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Placing ask order...\n',
    order = fighter.order(stock, 5100, 100, 'sell', 'limit')
    print '\t %s...\n' % str(order)[:40],
    print 'Placing bid order...\n',
    order = fighter.order(stock, 5100, 150, 'buy', 'limit')
    print '\t %s...\n' % str(order)[:40],
    _id = order['id']
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing quote...\n',
    quote = fighter.quote(stock)
    print '\t %s...\n' % str(quote)[:40],
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing order status...\n',
    status = fighter.order_status(stock, _id)
    print '\t %s...\n' % str(status)[:40]
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing order cancel...\n',
    order = fighter.cancel(stock, _id)
    print '\t %s...\n' % str(order)[:40],
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    print 'Testing list all orders...\n',
    orders = fighter.my_orders()
    print '\t %s...\n' % str(orders)[:40]
except Stockfighter.Exception as e:
    print e.status_code, e.error

try:
    import time
    print 'Waiting for keyboard interrupt'
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

