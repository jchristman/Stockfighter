Stockfighter
============

A python stockfighter API that can be used to play [Stockfighter](https://www.stockfighter.io/).

Please note that I'm being purposely vague in certain areas of documentation, as this is a learning environment and it will benefit you to read the documentation provided by Starfighters. Please, please, please read their [documentation](https://starfighter.readme.io/). This library provides ZERO assistance in regards to strategy - it will only hit API endpoints and perform functions if you ask it to.

That being said, if there are any improvements you feel could be made, please open an issue!

Requirements
============

This library is built on:

 * Python 2.7+
 * ws4py
 * requests

You should ```pip install``` the dependencies...

Setup
=====

The usage of this API is quite simple. If you simply fork this repository and then put your API key in the ```api``` file, that is all you should need to get going.

```
$ git clone https://github.com/jchristman/Stockfighter
$ cd Stockfighter
$ echo YOUR_API_KEY > api
```

Now the library is ready to use! My recommendation is to keep your levels in a different directory and symbolic link to stockfighter.py and api when you need them, or add the Stockfighter directory to your path.

Usage
=====

To get started, you will need to create a Stockfighter object. Most of these calls are used in the test.py script, so if you want an example of their usage, check that out.

```python
from stockfighter import Stockfighter

fighter = Stockfighter(VENUE, ACCOUNT) # Substitute the venue and account numbers here
```

But how do you get these values? You can either copy and paste them from the web UI, or you can use the API to start, resume, or restart a level. Each of these needs a parameter you may need to keep track of yourself. My suggestion is explore what the response to each of these methods is and see what information is returned by the servers to figure out how best to use these. Also, the endpoints for these functions are undocumented, so use them with caution. Also, note that **any function that fails in this API will raise a ```Stockfighter.Exception```**, which has an status_code and error field.

```python
# Note the these are static methods. You don't need a Stockfighter object to do these.
response = Stockfighter.start_level(NAME)   # The name of the level you want to start
response = Stockfighter.resume_level(ID)    # The numeric ID of the level you want to resume
response = Stockfighter.restart_level(ID)   # The numeric ID of the level you want to resume
response = Stockfighter.stop_level(ID)      # The numeric ID of the level you want to resume
response = Stockfighter.check_level(ID)     # The numeric ID of the level you want to resume
```

There are several health checks you can perform to test functionality.

```python
if fighter.heartbeat(): pass    # The heartbeat hits the API health check endpoint.
if fighter.check_venue(): pass  # Check the venue's health
```

Next come the various stock manipulation functions.

```python
symbols = fighter.list_stocks() # List the stocks available at a venue
orderbook = fighter.orderbook() # Get the current state of the orderbook

# This function should be studied carefully. Read the API documentation for stockfighter to
# determine what values you should be passing here.
status = fighter.order(STOCK, PRICE, QTY, DIRECTION, ORDER_TYPE)

quote = fighter.quote(STOCK)    # Pass a stock to get a quote
status = fighter.order_status(STOCK, ORDER_ID)  # Pass the stock and an order ID to get the current status
status = fighter.cancel(STOCK, ORDER_ID)        # Pass the stock and an order ID to cancel it
orders = fighter.my_orders()    # Get the status of all of your open orders
```

The websocket tickers are an important thing to understand, and this API provides a convenient way of the results from the websockets. Simply create a function that can handle quotes or executions coming in, then pass that function handle to the Stockfighter object and it will get called each time a new quote or execution comes over the socket. For example:

```python
def quote_ticker(quote):
    if quote is None: # The quote will be None if the websocket has died.
        fighter.quote_stock_ticker(quote_ticker, stock) # This will auto-restart the ticker if it dies
        return

    print '\t --- Quote from ticker: %s... ---\n' % str(quote)[:40],

def execution_ticker(execution):
    if execution is None:
        fighter.execution_stock_ticker(execution_ticker, stock) # This will auto-restart the ticker if it dies
        return

    print '\t --- Execution from ticker: %s... ---\n' % str(execution)[:40],

fighter.quote_ticker(quote_ticker)                      # This ticker will monitor all stocks on a venue
fighter.quote_stock_ticker(quote_ticker, stock)         # This ticker will monitor one stock on a venue
fighter.execution_ticker(execution_ticker)              # This ticker will monitor your executions on all stocks
fighter.execution_stock_ticker(execution_ticker, stock) # This ticker will monitor your executions on one stock
```

And that's about it! Happy stocking!
