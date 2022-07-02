from stockDatabase import StockDatabase

import statistics as stats
import datetime as dt

class TechnicalAnalysis(StockDatabase):

    # Returns the simple moving average for a date
    def getMovingAverage(self, ticker, date, n):
        closesList= self.getPriceHistoryColsBefore(ticker, "Close", date, n)
        movingAverage = sum([value[0] for value in closesList]) / n
        return movingAverage

    # Returns the Bollinger Bands for a date
    def getBollingerBands(self, ticker, date):
        closesList = self.getPriceHistoryColsBefore(ticker, "Close", date, 20)
        closes = [value[0] for value in closesList]
        movingAverage = sum(closes) / 20
        band = 2 * stats.stdev(closes)
        return [movingAverage - band, movingAverage, movingAverage + band]

    # Returns the Ichimoku Cloud indicators for a date
    # NOTE: The leading and lagging spans are not shifted
    def getIchimokuCloud(self, ticker, date):
        highs, lows = [[], []]
        histRows = self.getPriceHistoryColsBefore(ticker, "High, Low", date, 52)
        for row in histRows:
            highs.append(row[0])
            lows.append(row[1])
        max52, max26, max9 = max(highs), max(highs[:26]), max(highs[:9])
        min52, min26, min9 = min(lows), min(lows[:26]), min(lows[:9])
        conversionLine = (max9 + min9) / 2
        baseLine = (max26 + min26) / 2
        leadingSpanA = (conversionLine + baseLine) / 2
        leadingSpanB = (max52 + min52) / 2
        laggingSpan = self.getPriceHistoryOn(ticker, date)[0][4]
        return [leadingSpanA, leadingSpanB, conversionLine, baseLine, laggingSpan]

