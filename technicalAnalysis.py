from stockDatabase import StockDatabase

import statistics as stat
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
        band = 2 * stat.stdev(closes)

        movingAverage = sum(closes) / 20
        upperBand = movingAverage + band
        lowerBand = movingAverage - band

        return [upperBand, movingAverage, lowerBand]

    # Returns the Ichimoku Cloud indicators for a date
    # NOTE: The leading and lagging spans are not shifted
    def getIchimokuCloud(self, ticker, date):
        highs, lows = [[], []]
        histRows = self.getPriceHistoryColsBefore(ticker, "High, Low", date, 52)

        for row in histRows:
            highs.append(row[0])
            lows.append(row[1])

        max52, max26, max9 = max(highs), max(highs[:25]), max(highs[:8])
        min52, min26, min9 = min(lows), min(lows[:25]), min(lows[:8])

        conversionLine = (max9 + min9) / 2
        baseLine = (max26 + min26) / 2
        leadingSpanA = (conversionLine + baseLine) / 2
        leadingSpanB = (max52 + min52) / 2
        laggingSpan = self.getPriceHistoryOn(ticker, date)[0][4]

        return [leadingSpanA, leadingSpanB, conversionLine, baseLine, laggingSpan]

    # Returns the Donchian Channels for a date
    def getDonchianChannels(self, ticker, date):
        highs, lows = [[], []]
        histRows = self.getPriceHistoryColsBefore(ticker, "High, Low", date, 20)

        for row in histRows:
            highs.append(row[0])
            lows.append(row[1])

        upperChannel = max(highs)
        lowerChannel = min(lows)
        middleChannel = (upperChannel + lowerChannel) / 2

        return [upperChannel, middleChannel, lowerChannel]

    # Returns the RSI for a date
    # NOTE: Only returns the simplified equation result
    def getRSI(self, ticker, date):
        gains, losses = [[], []]
        histRows = self.getPriceHistoryColsBefore(ticker, "Open, Close", date, 14)

        for row in histRows:
            openPrice = row[0]
            closePrice = row[1]
            if closePrice > openPrice:
                gains.append(closePrice - openPrice)
            elif closePrice < openPrice:
                losses.append(openPrice - closePrice)

        rs = sum(gains) / sum(losses)
        rsi = 100 - (100 / (1 + rs))

        return rsi