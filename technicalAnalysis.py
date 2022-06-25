import statistics as stats
import datetime as dt

class TechnicalAnalysis:

    def __init__(self, db):
        self.db = db

    # Returns the simple moving average on a date
    def getMovingAverage(self, ticker, date, n):
        closes = self.db.execute("SELECT Close FROM '%s_history' WHERE Date < '%s' ORDER BY Date DESC LIMIT '%s'" % (ticker, date, n)).fetchall()
        movingAverage = sum([value[0] for value in closes]) / n
        return movingAverage

    # Returns the lower bound, moving average, and upper bound on a date
    def getBollingerBands(self, ticker, date, n=20):
        closes = self.db.execute("SELECT Close FROM '%s_history' WHERE Date < '%s' ORDER BY Date DESC LIMIT '%s'" % (ticker, date, n)).fetchall()
        closes = [value[0] for value in closes]
        movingAverage = sum(closes) / n
        band = 2 * stats.stdev(closes)
        return [movingAverage - band, movingAverage, movingAverage + band]
