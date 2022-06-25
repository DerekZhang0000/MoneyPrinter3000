from technicalAnalysis import TechnicalAnalysis

import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Chart(TechnicalAnalysis):

    def __init__(self, db):
        self.db = db

    def showChart(self, ticker, lowerDate, upperDate, **kwargs):

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(ticker, 'Volume'), vertical_spacing = 0.1, row_width = [0.2, 0.7])
        histRows = self.db.getTickerHistoryBetweenDates(ticker, lowerDate, upperDate)

        # Candlestick
        dates, opens, highs, lows, closes, volumes = [[], [], [], [], [], []]
        for row in histRows:
            dates.append(row[0])
            opens.append(row[1])
            highs.append(row[2])
            lows.append(row[3])
            closes.append(row[4])
            volumes.append(row[5])
        fig.add_trace(go.Candlestick(x=dates,
                                     open=opens,
                                     high=highs,
                                     low=lows,
                                     close=closes),
                      row = 1, col = 1)

        # Volume plot
        fig.add_trace(go.Bar(x = dates, y = volumes, showlegend=False),
                    row = 2, col = 1)

        # NOTE: getBollingerBands uses default n = 20
        if("bBands" not in kwargs.keys() or kwargs["bBands"] == True):
            lowerBand, movingAverage, upperBand = [[], [], []]

            for row in histRows:
                bollingerBands = self.getBollingerBands(ticker, row[0])
                lowerBand.append(bollingerBands[0])
                movingAverage.append(bollingerBands[1])
                upperBand.append(bollingerBands[2])

            # Moving Average
            fig.add_trace(go.Scatter(x = dates,
                                    y = movingAverage,
                                    line_color = 'black',
                                    name = 'sma'),
                        row = 1, col = 1)

            # Upper Bound
            fig.add_trace(go.Scatter(x = dates,
                                    y = upperBand,
                                    line_color = 'gray',
                                    line = {'dash': 'dash'},
                                    name = 'upper band',
                                    opacity = 0.5),
                        row = 1, col = 1)

            # Lower Bound
            fig.add_trace(go.Scatter(x = dates,
                                    y =  lowerBand,
                                    line_color = 'gray',
                                    line = {'dash': 'dash'},
                                    fill = 'tonexty',
                                    name = 'lower band',
                                    opacity = 0.5),
                        row = 1, col = 1)

        # Removes non-trading days
        startDate = dt.datetime.strptime(lowerDate, "%Y-%m-%d %H:%M:%S")
        endDate = dt.datetime.strptime(upperDate, "%Y-%m-%d %H:%M:%S")
        delta = endDate - startDate  # returns delta
        days = [(startDate + dt.timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(delta.days + 1)]
        dateGaps = [day for day in days if day not in dates]
        fig.update_xaxes(rangebreaks=[dict(values = dateGaps)])

        # Removes slider
        fig.update(layout_xaxis_rangeslider_visible=False)

        fig.show()