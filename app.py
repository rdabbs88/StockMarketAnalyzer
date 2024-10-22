from io import BytesIO
import base64
from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Creates an instance of the Flask application, "__name__" tells Flask where to look for resources like templates or static files
app = Flask(__name__)
application = app # Required by Elastic Beanstalk

# Function that retrieves historical data and plots it
def get_stock_data(ticker):

    # Initialize the Ticker object for the specified stock using yfinance
    stock = yf.Ticker(ticker)
    # Retrieve all available historical data for the stock
    data = stock.history(period="max")

    # Create a plot for the data
    plt.figure(figsize=(10,6))
    plt.plot(data.index, data["Close"], label="Closing Price", color="blue", linestyle="-")
    
    # Adding a title and labels to the X and Y axes
    plt.title(f"{ticker} Stock Price Over Time")
    plt.xlabel("Years")
    plt.ylabel("Price in $")
    plt.grid(True)
    plt.legend()
    #plt.show()

    # Save the graph to a BytesIO object (an in-memory buffer), encoded as base64 string which can be embedded in an HTML image tag
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url, stock

# Defining the route for the home page "/", accepting both GET and POST methods
# GET used to load the page and POST is used to submit the form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # retrieving the ticker symbol from the form submission
        ticker = request.form.get("ticker").upper()

        # Retrieve stock data and the plot URL
        plot_url, stock = get_stock_data(ticker)

        # grab the current stock price, open stock price, and closing stock price
        current_price = stock.info.get("currentPrice", "N/A")
        open_price = stock.info.get("open", "N/A")
        previous_close = stock.info.get("previousClose", "N/A")

        # rendering the HTML page, which the variables passed to the template
        return render_template("index.html",
                               plot_url=plot_url,
                               ticker=ticker,
                               current_price=current_price,
                               open_price=open_price,
                               previous_close=previous_close)

    # Handling GET requests, if the request method is GET, the tempate index.html is rendered without stock info
    return render_template("index.html")

# Running the Flask app, this starts the Flask development server in debug mode
if __name__ == "__main__":
    app.run(debug=True)