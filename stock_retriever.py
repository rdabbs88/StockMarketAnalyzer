import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# retrieves the current price, open price, and previous close price for the stock
def retrieve_stock_prices(ticker, stock):

    # grab the current stock price, open stock price, and closing stock price
    current_price = stock.info['currentPrice']
    open_price = stock.info['open']
    previous_close = stock.info['previousClose']

    print(f"Current Price of {ticker}: ${current_price}")
    print(f"Open Price of {ticker}: ${open_price}")
    print(f"Previous Close Price of {ticker}: ${previous_close}")

# displays historical data of the stock price
def display_stock_history(ticker, data):

    plt.figure(figsize=(10,6))
    plt.plot(data.index, data["Close"], label="Closing Price", color="blue", linestyle="-")
    
    # Adding a title and labels to the X and Y axes
    plt.title(f"{ticker} Stock Price Over Time")
    plt.xlabel("Years")
    plt.ylabel("Price in $")
    plt.grid(True)
    plt.legend()

    plt.show()


# returns all the keys that exist and are available in our dictionary
def search_key_by_keyword(data: dict, keyword: str) -> list[str]:
    return list(filter(lambda x: keyword in x.lower(), data.keys()))

# Main
def main():
    # Prompt user for a Ticker symbol
    ticker_input = input("Enter a Stock Ticker symbol to retrieve its price: ")

    # Initialize the Ticker object for the specified stock
    stock = yf.Ticker(ticker_input)
    # Retrieve all available historical data
    historical_data = stock.history(period="max")

    ''' Useful link: https://github.com/ranaroussi/yfinance/issues/1519
    # printing out the available keys with the keyword market
    valid_market_keys = search_key_by_keyword(stock.info, "market")
    print(valid_market_keys)
    # printing out the available keys with the keyword current
    valid_market_keys = search_key_by_keyword(stock.info, "current")
    print(valid_market_keys)
    # printing out the available keys with the keyword high
    valid_market_keys = search_key_by_keyword(stock.info, "high")
    print(valid_market_keys)
    '''

    display_stock_history(ticker_input, historical_data)
    retrieve_stock_prices(ticker_input, stock)

# Entry point of the script
if __name__ == "__main__":
    main()