## Stock Market Prediction using Random Forest
This project predicts stock prices using a **Random Forest Regressor**, a robust machine learning model for regression tasks. The system fetches real stock data, extracts key indicators, trains the model, and visualizes predictions on a dynamic web dashboard.
---

## 🚀 Features
- Predicts the next day’s stock price using Random Forest.
- Fetches live stock data from **Yahoo Finance**.
- Generates **technical indicators**: SMA, RSI, and MACD.
- Web-based visualization using **Flask** and **Chart.js**.
- Includes an interactive chart with **play/pause animation**.
- Users can **download predicted data as CSV**.

---
## 🧩 Workflow

### 1. Data Collection
- Uses the `yfinance` library to fetch 1-year historical data.
- Extracts features such as `Open`, `Close`, `High`, `Low`, and `Volume`.

### 2. Feature Engineering
Adds technical indicators using `TA-Lib`:
- **SMA (Simple Moving Average)**
- **RSI (Relative Strength Index)**
- **MACD (Moving Average Convergence Divergence)**

### 3. Model Training
- **Model**: `RandomForestRegressor` from scikit-learn.
- **Target**: Predict the next day’s closing price.
- **Split**: 80% training, 20% testing.
- Model is saved as `stock_model.pkl` for prediction.

### 4. Model Prediction
- Loads the trained model.
- Uses the latest data (SMA, RSI, MACD) to predict future prices.
- Returns predicted stock prices as JSON via Flask API.

### 5. Web Integration
**Flask API Endpoints:**
- `/api/historical_data`: Returns historical stock data.
- `/api/predict`: Returns predicted prices for the next 30 days.

**Frontend (HTML/CSS/JS):**
- Displays stock data in a scrollable table.
- Uses **Chart.js** for animated line graphs.
- User controls for play/pause and animation speed.

---

## 📊 Example Evaluation (Sample)
| Metric | Random Forest |
|--------|----------------|
| R² | -0.33 |
| MAE | 8.42 |
| RMSE | 13.22 |

> The model works but underperforms compared to deep learning models like LSTM.

---

## ⚙️ Installation & Usage
```bash
# Clone this repository
git clone https://github.com/yourusername/stock-market-rf.git
cd stock-market-rf

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

Then open http://127.0.0.1:5000 in your browser.

---

## 🔍 Key Components

Backend: Flask, scikit-learn, pandas, TA-Lib, yfinance

Frontend: HTML, CSS, JavaScript, Chart.js

Data: Real market data from Yahoo Finance

---

## 🧠 Learnings

Implemented data preprocessing and feature extraction for ML models.

Explored Random Forest for financial time-series regression.

Integrated model into an interactive web dashboard.


---

## 🏁 Conclusion

While Random Forest provides a good baseline for stock prediction, the results show that LSTM networks outperform traditional ML models in capturing time-dependent financial patterns. This project serves as a solid introduction to end-to-end stock market prediction and visualization.

---

# Acknowledgments
Thanks to my mentors and colleagues for their guidance.

---

## 📄 License
This project is for academic and demonstration purposes only. Please credit the authors if reused or modified.
