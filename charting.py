from technicalAnalysis import TechnicalAnalysis

import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Chart(TechnicalAnalysis):

    def showChart(self, ticker, lowerDate, upperDate, **kwargs):

        curRow = 1
        plotRows = 1
        rowWidths = [0.7]
        plotTitles = [ticker]
        if ("vol" not in kwargs.keys() or kwargs["vol"] == True):
            plotRows += 1
            plotTitles.append("Volume")
            rowWidths.insert(0, 0.1)
        if ("rsi" not in kwargs.keys() or kwargs["rsi"] == True):
            plotRows +=1
            plotTitles.append("RSI")
            rowWidths.insert(0, 0.1)
        # if ("macd" not in kwargs.keys() or kwargs["macd"] == True):
        #     plotRows += 1
        #     plotTitles.append("MACD")
        #     rowWidths.insert(0, 0.1)

        # Initializing common values
        dates, opens, highs, lows, closes, volumes = [[], [], [], [], [], []]
        histRows = self.getPriceHistoryBetween(ticker, lowerDate, upperDate)
        for row in histRows:
            dates.append(row[0])
            opens.append(row[1])
            highs.append(row[2])
            lows.append(row[3])
            closes.append(row[4])
            volumes.append(row[5])
       
        # Initializing chart
        fig = make_subplots(rows=plotRows, cols=1, shared_xaxes=True, subplot_titles=plotTitles, vertical_spacing=0.1, row_width=rowWidths)

        # Candlestick chart, always displayed
        fig.append_trace(go.Candlestick(x=dates,
                                        open=opens,
                                        high=highs,
                                        low=lows,
                                        close=closes,
                                        name="Candlestick"),
                         row=1, col=1)

        # Volume chart
        if ("vol" not in kwargs.keys() or kwargs["vol"] == True):
            curRow += 1
            fig.append_trace(go.Bar(x=dates,
                                    y=volumes,
                                    showlegend=False,
                                    name="Volume"),
                             row=curRow, col=1)

        # RSI
        # NOTE: Uses simplified 14-day method of calculation
        if ("rsi" not in kwargs.keys() or kwargs["rsi"] == True):
            curRow += 1
            rsi = [self.getRSI(ticker, date) for date in dates]
            fig.append_trace(go.Scatter(x=dates,
                                        y=rsi,
                                        showlegend=False,
                                        line_color="mediumvioletred",
                                        name="RSI (Simplified)"),
                             row=curRow, col=1)

        # MACD
        if ("macd" not in kwargs.keys() or kwargs["macd"] == True):
            curRow += 1
            # fig.append_trace(go.Bar(x=dates, y=volumes, showlegend=False),
            #                         row=curRow, col=1)

        # Simple Moving Averages
        if("smas" not in kwargs.keys() or kwargs["smas"] == True):
            fastMovingAverage, slowMovingAverage = [[], []]

            for date in dates:
                fastMovingAverage.append(self.getMovingAverage(ticker, date, 50))
                slowMovingAverage.append(self.getMovingAverage(ticker, date, 200))

            # 50 Day SMA
            fig.append_trace(go.Scatter(x=dates,
                                    y=fastMovingAverage,
                                    line_color='orange',
                                    name='50MA'),
                             row=1, col=1)

            # 200 Day SMA
            fig.append_trace(go.Scatter(x=dates,
                                     y=slowMovingAverage,
                                     line_color='blue',
                                     name='200MA'),
                             row=1, col=1)

        # Bollinger Bands
        if("bands" not in kwargs.keys() or kwargs["bands"] == True):
            lowerBand, movingAverage, upperBand = [[], [], []]

            for row in histRows:
                bollingerBands = self.getBollingerBands(ticker, row[0])
                lowerBand.append(bollingerBands[0])
                movingAverage.append(bollingerBands[1])
                upperBand.append(bollingerBands[2])

            # Moving Average (middle band)
            fig.append_trace(go.Scatter(x=dates,
                                    y=movingAverage,
                                    line_color='goldenrod',
                                    name='20MA'),
                             row=1, col=1)

            # Upper Band
            fig.append_trace(go.Scatter(x=dates,
                                    y=upperBand,
                                    line_color='blueviolet',
                                    name='Upper Band',
                                    opacity=0.5),
                             row=1, col=1)

            # Lower Band
            fig.append_trace(go.Scatter(x=dates,
                                    y=lowerBand,
                                    line_color='blueviolet',
                                    name='Lower Band',
                                    opacity=0.5),
                             row=1, col=1)

        # Ichimoku Cloud
        # NOTE: Leading and lagging spans are not shifted
        if("cloud" not in kwargs.keys() or kwargs["cloud"] == True):
            leadingSpanA, leadingSpanB, conversionLine, baseLine, laggingSpan = [[], [], [], [], []]

            for row in histRows:
                ichimokuCloud = self.getIchimokuCloud(ticker, row[0])
                leadingSpanA.append(ichimokuCloud[0])
                leadingSpanB.append(ichimokuCloud[1])
                conversionLine.append(ichimokuCloud[2])
                baseLine.append(ichimokuCloud[3])
                laggingSpan.append(ichimokuCloud[4])

            # Leading Span A
            fig.append_trace(go.Scatter(x=dates,
                                    y=leadingSpanA,
                                    line_color='green',
                                    name='Leading Span A'),
                             row=1, col=1)

            # Leading Span B
            fig.append_trace(go.Scatter(x=dates,
                                    y=leadingSpanB,
                                    line_color='red',
                                    name='Leading Span B'),
                             row=1, col=1)

            # Conversion Line
            fig.append_trace(go.Scatter(x=dates,
                                    y=conversionLine,
                                    line_color='salmon',
                                    name='Conversion Line'),
                             row=1, col=1)

            # Base Line
            fig.append_trace(go.Scatter(x=dates,
                                    y=baseLine,
                                    line_color='gray',
                                    name='Base Line',
                                    opacity=0.5),
                             row=1, col=1)

            # Lagging Span
            fig.append_trace(go.Scatter(x=dates,
                                    y=laggingSpan,
                                    line_color='purple',
                                    name='Lagging Span',
                                    opacity=0.5),
                             row=1, col=1)

        # Donchian Channels
        if("channels" not in kwargs.keys() or kwargs["channels"] == True):
            upperChannel, middleChannel, lowerChannel = [[], [], []]

            for row in histRows:
                donchianChannels = self.getDonchianChannels(ticker, row[0])
                upperChannel.append(donchianChannels[0])
                middleChannel.append(donchianChannels[1])
                lowerChannel.append(donchianChannels[2])

            # Upper Channel
            fig.append_trace(go.Scatter(x=dates,
                                    y=upperChannel,
                                    line_color='gold',
                                    name='Upper Channel'),
                             row=1, col=1)

            # Middle Channel
            fig.append_trace(go.Scatter(x=dates,
                                    y=middleChannel,
                                    line_color='greenyellow',
                                    name='Middle Channel',
                                    opacity=0.5),
                             row=1, col=1)

            # Lower Channel
            fig.append_trace(go.Scatter(x=dates,
                                    y=lowerChannel,
                                    line_color='gold',
                                    name='Lower Channel',
                                    opacity=0.5),
                             row=1, col=1)
            
        # Financial Events
        if("earnings" not in kwargs.keys() or kwargs["earnings"] == True):
            events = self.getFinancialEventHistory(ticker)
            for event in events:
                if event[0][:11] + "00:00:00" in dates:
                    fig.add_vline(x=dt.datetime.strptime(event[0][:11] + "00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000,line_width=3, row=1, col=1, line_color='rgba(0, 0, 0, 0.075)', annotation=dict(text="EPS EST.: " + str(event[1]) + "<br>EPS ACT.: " + str(event[2]) + "<br>Surprise: " + str(event[3] * 100) + "%", showarrow=False, font=dict(color='black', size=8)))

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