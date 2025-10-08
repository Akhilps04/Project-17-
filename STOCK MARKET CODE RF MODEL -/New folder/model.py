import yfinance as yf
import pandas as pd
import talib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import numpy as np

# Fetch stock data
def fetch_stock_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Flatten the MultiIndex by selecting the second level (the ticker symbol)
    data.columns = data.columns.droplevel(1)  # Dropping the 'Ticker' level from the MultiIndex
    
    # Print the columns to check if 'Close' exists
    print("Columns in the downloaded data:", data.columns)

    # Ensure 'Close' exists, or fallback to 'Adj Close'
    if 'Close' not in data.columns:
        if 'Adj Close' in data.columns:
            print("Using 'Adj Close' as 'Close' column is missing.")
            data['Close'] = data['Adj Close']  # Fallback to 'Adj Close'
        else:
            raise KeyError("Neither 'Close' nor 'Adj Close' column found in data")
    
    return data

# Feature Engineering (Technical Indicators)
def add_technical_indicators(data):
    # Drop rows with NaN values in 'Close' column
    data = data.dropna(subset=['Close'])

    # Ensure we are using a 1D array
    close_prices = data['Close'].values  # This ensures it's a 1D NumPy array

    # Check if the array has only one dimension
    if close_prices.ndim != 1:
        print("Error: The close_prices array is not 1D")
        return data
    
    data['SMA'] = talib.SMA(close_prices, timeperiod=14)
    data['RSI'] = talib.RSI(close_prices, timeperiod=14)
    data['MACD'], data['MACD_signal'], _ = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    
    return data.dropna()  # Drop rows with NaN values generated during TA-Lib computation


# Prepare the data for Random Forest
def prepare_data(data):
    features = ['SMA', 'RSI', 'MACD']
    data['Price'] = data['Close'].shift(-1)  # Predict next day's price
    data = data.dropna()  # Drop rows with missing values
    X = data[features]
    y = data['Price']
    return train_test_split(X, y, test_size=0.2, shuffle=False)

# Train Random Forest Model
def train_model(stock_symbol):
    data = fetch_stock_data(stock_symbol, '2020-01-01', '2022-01-01')
    data = add_technical_indicators(data)
    X_train, X_test, y_train, y_test = prepare_data(data)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the trained model
    with open('stock_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model trained and saved!")
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(y_pred)
    print(y_test)

    # Calculate the evaluation metrics
    mae = mean_absolute_error(y_test, y_pred) # Mean absolute error
    mse = mean_squared_error(y_test, y_pred) # Mean squared error
    rmse = np.sqrt(mse) # Root mean squared error
    r2 = r2_score(y_test, y_pred) # R-squared score


     # Print the evaluation metrics
    print(f"Model Evaluation:")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R-squared Score: {r2}")

train_model('AAPL')  # Example: Train for Apple
