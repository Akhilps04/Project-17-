from flask import Flask, render_template, request, jsonify
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)

def get_prediction(stock_symbol):
    # In a real app, this would involve your trained model
    # For now, let's just return some placeholder data
    # showing a simple upward trend for demonstration.
    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(30)][::-1] # Last 30 days
    predicted_prices = [100 + i * 0.5 + (i % 5) * 2 - (i % 3) * 1 for i in range(30)] # Simple trend
    return {"dates": [d.strftime('%Y-%m-%d') for d in dates], "prices": predicted_prices}

def get_historical_data(stock_symbol, period='1y'):
    try:
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return None
        hist = hist[['Close']].reset_index()
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        return hist.to_dict(orient='records')
    except Exception as e:
        print(f"Error fetching historical data for {stock_symbol}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    stock_symbol = request.json.get('stockSymbol', 'AAPL') # Default to AAPL
    prediction_data = get_prediction(stock_symbol)
    return jsonify(prediction_data)

@app.route('/api/historical_data', methods=['POST'])
def historical_data():
    stock_symbol = request.json.get('stockSymbol', 'AAPL')
    period = request.json.get('period', '1y')
    data = get_historical_data(stock_symbol, period)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Could not fetch historical data"}), 404

if __name__ == '__main__':
    app.run(debug=True)