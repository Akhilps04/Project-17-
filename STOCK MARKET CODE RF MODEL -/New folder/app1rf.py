import pickle
from flask import Flask, render_template, request, jsonify
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import talib

app = Flask(__name__)

# Load the trained model
with open('stock_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to fetch historical data
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

# Feature extraction for prediction
def add_technical_indicators(data):
    data['SMA'] = talib.SMA(data['Close'], timeperiod=14)
    data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
    data['MACD'], data['MACD_signal'], _ = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return data.dropna()

# Prediction function
def get_prediction(stock_symbol):
    try:
        # Simulate a prediction for the next 30 days (you can replace this with your model's prediction)
        today = datetime.now()
        dates = [today + timedelta(days=i) for i in range(30)]  # Predict for next 30 days
        predicted_prices = [100 + i * 0.5 + (i % 5) * 2 - (i % 3) * 1 for i in range(30)]  # Simulated prediction

        # Return simulated predicted data (dates and prices)
        return {"dates": [d.strftime('%Y-%m-%d') for d in dates], "prices": predicted_prices}
    except Exception as e:
        print(f"Error in prediction: {e}")
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    stock_symbol = request.json.get('stockSymbol', 'AAPL')  # Default to AAPL
    prediction_data = get_prediction(stock_symbol)
    return jsonify(prediction_data)

# New route for historical data
@app.route('/api/historical_data', methods=['POST'])
def historical_data():
    stock_symbol = request.json.get('stockSymbol', 'AAPL')  # Default to AAPL
    period = request.json.get('period', '1y')  # Default to 1 year
    data = get_historical_data(stock_symbol, period)
    
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Could not fetch historical data"}), 404

if __name__ == '__main__':
    app.run(debug=True)
