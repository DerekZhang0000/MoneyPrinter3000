from technicalAnalysis import TechnicalAnalysis

import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Chart(TechnicalAnalysis):

    def __init__(self, db):
        self.db = db

    def showChart(self, ticker, lowerDate, upperDate, **kwargs):

        curRow = 1
        plotRows = 1
        rowWidths = [0.7]
        plotTitles = [ticker]
        if ("vol" not in kwargs.keys() or kwargs["vol"] == True):
            plotRows += 1
            plotTitles.append("Volume")
            rowWidths.insert(0, 0.1)
        # if ("rsi" not in kwargs.keys() or kwargs["rsi"] == True):
        #     plotRows +=1
        #     plotTitles.append("RSI")
        #     rowWidths.insert(0, 0.1)
        # if ("macd" not in kwargs.keys() or kwargs["macd"] == True):
        #     plotRows += 1
        #     plotTitles.append("MACD")
        #     rowWidths.insert(0, 0.1)
        fig = make_subplots(rows=plotRows, cols=1, shared_xaxes=True, subplot_titles=plotTitles, vertical_spacing=0.1, row_width=rowWidths)
        histRows = self.db.getTickerHistoryBetweenDates(ticker, lowerDate, upperDate)

        # Initializing common values
        dates, opens, highs, lows, closes, volumes = [[], [], [], [], [], []]
        for row in histRows:
            dates.append(row[0])
            opens.append(row[1])
            highs.append(row[2])
            lows.append(row[3])
            closes.append(row[4])
            volumes.append(row[5])

        # Candlestick chart, always displayed
        fig.append_trace(go.Candlestick(x=dates,
                                     open=opens,
                                     high=highs,
                                     low=lows,
                                     close=closes),
                         row=1, col=1)

        # Volume chart
        if ("vol" not in kwargs.keys() or kwargs["vol"] == True):
            curRow += 1
            fig.append_trace(go.Bar(x=dates, y=volumes, showlegend=False),
                                    row=curRow, col=1)

        if ("rsi" not in kwargs.keys() or kwargs["rsi"] == True):
            curRow += 1
            # fig.append_trace(go.Bar(x=dates, y=volumes, showlegend=False),
            #                         row=curRow, col=1)

        if ("macd" not in kwargs.keys() or kwargs["macd"] == True):
            curRow += 1
            # fig.append_trace(go.Bar(x=dates, y=volumes, showlegend=False),
            #                         row=curRow, col=1)

        # Bollinger bands, uses default n=20
        if("bBands" not in kwargs.keys() or kwargs["bBands"] == True):
            lowerBand, movingAverage, upperBand = [[], [], []]

            for row in histRows:
                bollingerBands = self.getBollingerBands(ticker, row[0])
                lowerBand.append(bollingerBands[0])
                movingAverage.append(bollingerBands[1])
                upperBand.append(bollingerBands[2])

            # Moving Average (middle band)
            fig.append_trace(go.Scatter(x=dates,
                                    y=movingAverage,
                                    line_color='red',
                                    name='20MA'),
                             row=1, col=1)

            # Upper Bound
            fig.append_trace(go.Scatter(x=dates,
                                    y=upperBand,
                                    line_color='lightblue',
                                    name='Upper Band',
                                    opacity=0.5),
                             row=1, col=1)

            # Lower Bound
            fig.append_trace(go.Scatter(x=dates,
                                    y=lowerBand,
                                    line_color='lightblue',
                                    fill='tonexty',
                                    name='Lower Band',
                                    opacity=0.5),
                             row=1, col=1)

        # Simple moving average, uses default n=50, n=200
        if("smas" not in kwargs.keys() or kwargs["smas"] == True):
            fastMovingAverage, slowMovingAverage = [[], []]

            for date in dates:
                fastMovingAverage.append(self.getMovingAverage(ticker, date, 50))
                slowMovingAverage.append(self.getMovingAverage(ticker, date, 200))

            fig.append_trace(go.Scatter(x=dates,
                                    y=fastMovingAverage,
                                    line_color='orange',
                                    name='50MA'),
                             row=1, col=1)

            fig.append_trace(go.Scatter(x=dates,
                                     y=slowMovingAverage,
                                     line_color='blue',
                                     name='200MA'),
                             row=1, col=1)

        # Removes non-trading days
        startDate = dt.datetime.strptime(lowerDate, "%Y-%m-%d %H:%M:%S")
        endDate = dt.datetime.strptime(upperDate, "%Y-%m-%d %H:%M:%S")
        delta = endDate - startDate
        days = [(startDate + dt.timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S") for d in range(delta.days + 1)]
        dateGaps = [day for day in days if day not in dates]
        fig.update_xaxes(rangebreaks=[dict(values = dateGaps)])

        # Removes slider
        fig.update(layout_xaxis_rangeslider_visible=False)

        fig.show()