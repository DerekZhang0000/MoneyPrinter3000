import sqlite3 as sql
import yfinance as yf
import pandas as pd

class StockDatabase:

    # Methods for StockDatabase initialization
    def __init__(self):
        self.connection = sql.connect("stockData.db")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.commit()
        self.close()

    # Methods based on sqlite3
    def connect(self):
        self.connection = sql.connect("stockData.db")
        self.cursor = self.connection.cursor()

    def execute(self, command):
        return self.cursor.execute(command)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    # Load ticker history into database
    def loadTickerHistory(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            self.cursor.execute('DROP TABLE IF EXISTS %s_history' % ticker)
            df = yf.Ticker(ticker).history(period="max", interval="1d")
            df.to_sql(name=ticker+"_history", con=self.connection)
            data = pd.read_sql("SELECT * FROM %s_history" % ticker, con=self.connection)
            data.Date = pd.to_datetime(data.Date)
            data.set_index('Date')
        self.connection.commit()

    # Updates ticker history, or creates new table if not existing
    def updateTickerHistory(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            tableFound = self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s_history'" % ticker).fetchone() != None
            if not tableFound:
                self.loadTickerHistory(self, ticker)
                return
            df = yf.Ticker(ticker).history(period="max", interval="1d")
            dbRows = self.execute("SELECT COUNT(*) FROM '%s_history'" % ticker).fetchone()[0]
            dfRows = len(df.index)
            diffTable = df.iloc[dbRows:dfRows]
            diffRows = list(diffTable.itertuples(index=True, name=None))
            for i in range(len(diffTable.index)):
                row = tuple([str(diffRows[i][0])] + list(diffRows[i][1:]))
                self.cursor.execute("INSERT INTO '%s_history' VALUES(?,?,?,?,?,?,?,?)" % row)
            self.connection.commit()

    # Returns history (single row) of a given ticker on a specific date
    def getTickerHistoryOnDate(self, ticker, date):
        return self.execute("SELECT * FROM %s_history WHERE Date = '%s'" % (ticker, date)).fetchall()

    # Returns history between two dates (inclusive)
    def getTickerHistoryBetweenDates(self, ticker, lowerDate, upperDate):
        return self.execute("SELECT * FROM %s_history WHERE Date BETWEEN '%s' AND '%s'" % (ticker, lowerDate, upperDate)).fetchall()
