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
    def loadPriceHistory(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            self.cursor.execute("DROP TABLE IF EXISTS {}_Price_History".format(ticker))
            df = yf.Ticker(ticker).history(period="max", interval="1d")
            df.to_sql(name=ticker+"_Price_History", con=self.connection)
            data = pd.read_sql("SELECT * FROM {}_Price_History".format(ticker), con=self.connection)
            data.Date = pd.to_datetime(data.Date)
            data.set_index('Date')
        self.connection.commit()
        
    # Load ticker financial event history into database
    def loadFinancialHistory(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            self.cursor.execute("DROP TABLE IF EXISTS {}_Financial_Events".format(ticker))

            df = yf.Ticker(ticker).earnings_dates
            df.to_sql(name=ticker+"_Financial_Events", con=self.connection)
            data = pd.read_sql("SELECT * FROM {}_Financial_Events".format(ticker), con=self.connection)
            data.Date = pd.to_datetime(data.Date)
            data.set_index('Date')
        self.connection.commit()

    # Updates ticker price history, or creates new table if not existing
    def updatePriceHistory(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            tableFound = self.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{}_Price_History'".format(ticker)).fetchone() != None
            if not tableFound:
                self.loadPriceHistory(ticker)
                return
            df = yf.Ticker(ticker).history(period="max", interval="1d")
            dbRows = self.execute("SELECT COUNT(*) FROM {}_Price_History".format(ticker)).fetchone()[0]
            dfRows = len(df.index)
            diffTable = df.iloc[dbRows:dfRows]
            diffRows = list(diffTable.itertuples(index=True, name=None))
            for i in range(len(diffTable.index)):
                row = tuple([str(diffRows[i][0])] + list(diffRows[i][1:]))
                print("INSERT INTO {}_Price_History VALUES {}".format(ticker, row))
                self.cursor.execute("INSERT INTO {}_Price_History VALUES {}".format(ticker, row))
            self.connection.commit()
    
    # Updates the dates of significant events for the given ticker, or creates a new table if not existing
    def updateFinancialEvents(self, tickerList):
        if type(tickerList) != list:
            tickerList = [tickerList]
        for ticker in tickerList:
            tableFound = self.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{}_Financial_Events'".format(ticker)).fetchone() != None
            if not tableFound:
                self.loadFinancialHistory(ticker)
                return
            df = yf.Ticker(ticker).earnings_dates
            dbRows = self.execute("SELECT COUNT(*) FROM {}_Financial_Events".format(ticker)).fetchone()[0]
            dfRows = len(df.index)
            diffTable = df.iloc[dbRows:dfRows]
            diffRows = list(diffTable.itertuples(index=True, name=None))
            for i in range(len(diffTable.index)):
                row = tuple([str(diffRows[i][0])] + list(diffRows[i][1:]))
                print("INSERT INTO {}_Financial_Events VALUES {}".format(ticker, row))
                self.cursor.execute("INSERT INTO {}_Financial_Events VALUES {}".format(ticker, row))
            self.connection.commit()
            
        

    # Returns ticker history (single row) of a given ticker on a specific date
    def getPriceHistoryOn(self, ticker, date):
        return self.execute("SELECT * FROM {}_Price_History WHERE Date <= '{}' ORDER BY Date DESC LIMIT 1".format(ticker, date)).fetchall()

    # Returns ticker history between two dates (inclusive)
    def getPriceHistoryBetween(self, ticker, lowerDate, upperDate):
        return self.execute("SELECT * FROM {}_Price_History WHERE Date BETWEEN '{}' AND '{}'".format(ticker, lowerDate, upperDate)).fetchall()

    # Returns ticker history before a date with a limit (exclusive)
    def getPriceHistoryBefore(self, ticker, date, limit):
        return self.execute("SELECT * FROM {}_Price_History WHERE Date < '{}' ORDER BY Date DESC LIMIT {}".format(ticker, date, limit)).fetchall()

    # Returns column(s) of a ticker history before a date with a limit (exclusive)
    def getPriceHistoryColsBefore(self, ticker, columns, date, limit):
        return self.execute("SELECT {} FROM {}_Price_History WHERE Date < '{}' ORDER BY Date DESC LIMIT {}".format(columns, ticker, date, limit)).fetchall()

    # Returns the ticker's financial event history
    def getFinancialEventHistory(self, ticker):
        return self.execute("SELECT * FROM {}_Financial_Events".format(ticker)).fetchall()
    