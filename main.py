# Tasks:
# 1. Load stock data DONE
# 1.5 Make function to insert one row of a stock, not replace the whole thing DONE
# 2. Create functions for technical indicators
# 2.01 Moving Averages DONE
# 2.1 Bollinger bands DONE
# 2.2 Ice cream clouds DONE
# 2.25 Donchian channels DONE
# 2.3 RSI DONE, MACD, Parabolic SAR, SuperTrend, Aroon, Coppock Curve,
#     Detrended Price Oscillator, Elliot Wave Oscillator, Money Flow Index,
#     TTM Squeeze, Vortex Oscillator
# 3. Identify days of high confidence of price movement (and also magnitude of the movement)
# 4. Calculate implied probabilities / price movements with options data
# 5. Create machine learning algorithm to test against / with this

from stockDatabase import StockDatabase
from technicalAnalysis import TechnicalAnalysis
from charting import Chart

from datetime import date

currentDate = str(date.today()) + " 00:00:00"
db, ta, chart = StockDatabase(), TechnicalAnalysis(), Chart()

# Main
# db.updatePriceHistory('TSLA')
# print(ta.getRSI("TSLA", "2022-07-01 00:00:00"))
chart.showChart("TSLA", "2020-06-20 00:00:00", currentDate)
# ta.getIchimokuCloud("TSLA", currentDate)
# print(ta.movingAverage("TSLA", currentDate, 20))
# print(ta.getBollingerBands("TSLA", currentDate, 20))