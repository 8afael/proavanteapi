import yfinance as yf
from pprintpp import pprint
import pandas as pd

class Yahoo:
    def __init__(self, ticker, startDate, endDate):
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate

    def getDividends(self):
        try:
            dividends = yf.download(self.ticker, self.startDate, self.endDate, actions=True)
            if dividends.empty:
                print('Verify connection')
                #pprint(dividends)
            else:
                divNoZero = dividends.loc[dividends.Dividends !=0]
                sumDividends = dividends['Dividends'].sum()
                pprint(divNoZero)
                pprint(f'Total Dividends: {sumDividends}')
                return sumDividends

        except Exception as e:
            print(f"Error: {e}")

    def setYears(self, time):
        dividends = self.getDividends()
        if time == 3:
            dividends = dividends/3
            print(f' 3 years: {dividends}')
            return dividends
        elif time == 5:
            dividends = dividends/5
            print(f' 5 years: {dividends}')
            return dividends
        elif time == 10:
            dividends = dividends/10
            print(f' 10 years: {dividends}')
            return dividends
        else:
            return print(f"1 year: {dividends}")

    def getDyAnnual(self):
        ticker_data = yf.Ticker(self.ticker).history(start=self.startDate, end=self.endDate)
        dividend_yield = ticker_data['Dividends'].mean()  # Calculate the average dividend yield for the year
        print(f"Dividend yield for {self.ticker} in 2023: {dividend_yield * 100:.2f}%")


runClass = Yahoo("PETR4.SA", "2023-08-09", "2024-08-09")
runClass.getDividends()
#runClass.getDyAnnual()
runClass.setYears(1)