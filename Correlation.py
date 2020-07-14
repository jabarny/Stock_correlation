import datetime as dt
import numpy as np
import pandas as pd
import re

import yfinance as yf,

"""a script that retrieves stock price history creating an
    excel file of the stocks' correlation in the process; 

    1) func - aggregates stocks and adj close, prints them; returns dataframe
    2) func -  adds stock returns to a dataframe; returns dataframe
    3) func - creates correlation DF and writes to excel file; return None
    4) func - call all functions
        
    """


# create dataframe of stocks
def stock_df():
    """aggregates the stocks Adj Close, prints them"""

    while 1:
        start_date = input('Enter start date in "YYYY-MM-DD" format (or "default" for last 5 years): ').lower()
        end_date = input('Enter date in "YYYY-MM-DD" format (or "default" for present day): ').lower()

        # ensure proper 'YYYY-MM-DD' format
        pattern = "(([0-9]){4}-([0-9]){2}-([0-9]){2})|(default)"
        if re.match(pattern, start_date) and re.match(pattern, end_date):
            break
        else:
            print(f'If not seeking the "default" dates, ensure both "{start_date}" and "{end_date}" match the "YYYY-MM-DD" format')
            continue

    # timeframe
    if start_date == 'default':
        start_date = str(dt.datetime.today() - dt.timedelta(weeks=260))[:10]
    if end_date == 'default':
        end_date = dt.datetime.today().strftime('%Y-%m-%d')
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
    print(data)
    return data

# transform stock returns
def stock_returns(data=None):
    """adds the stocks returns to a dataframe"""
    returns = pd.DataFrame()
    for stocks in data:
        if stocks not in returns:
            returns[stocks] = np.log(data[stocks]).diff()
    print(returns[1:].dropna())
    return returns[1:]


def corr_matrix(df=None):
    """ create correlation matrix & writes to excel file """
    print(df.corr())
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    # to excel
    df.corr().dropna().to_excel('Correlation.xlsx', sheet_name='Stock_correlation')
    return df.corr()


def stock_corr():
    """calls all functions"""
    data = stock_df()
    df = stock_returns(data=data)
    corr_matrix(df)


stocks = ['SPY',]

while 1:
    resp = input('Enter tickersymbol (\'exit\' to exit prompt): ').strip().upper()
    if re.match('EXIT', resp):
        break
    elif re.search('([^A-Z\.])+', resp):
        # filters most of the invalid responses. won't catch multiple ".." in the response
        print(f'{resp} containes an invalid character(s); must only contain (up to 8 letters)')
    elif re.match('[A-Z.?]{1,8}', resp):
        stocks.append(resp)
    else:
        print(f'Ensure "{resp}" contains ONLY A-Z characters, regardless of capitalization; no integers, spaces, punctuations. ')        

stock_corr()
