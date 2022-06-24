# Tasks:
# 1. Load stock data DONE
# 1.5 Make function to insert one row of a stock, not replace the whole thing
# 2. Create functions for technical indicators
# 3. Identify days of high confidence of price movement (and also magnitude of the movement)
# 4. Calculate implied probabilities / price movements with options data
# 5. Create machine learning algorithm to test against / with this

from stockDatabase import StockDatabase
import ta

from datetime import date
import pendulum as pen
import matplotlib.pyplot as plt

currentDate = str(date.today()) + " 00:00:00"
db = StockDatabase()
TICKER = "OPEN"

# Main
# db.loadTickerHistory(TICKER)
# db.loadTickerHistory(["MSFT", "NVDA", "SPY", "UVXY", "CBOE", "AMD", "MANT", "SPCE"])
# print(*db.getTickerHistoryOnDate(TICKER, currentDate))
db.updateTickerHistory(TICKER)
