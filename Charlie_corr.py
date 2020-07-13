import yfinance as yf, numpy as np, pandas as pd

"""a charlie-centered script that creates three individual functions and one function that calls all three, creating an
    excel file in the process; 

    1) func - aggregates stocks and adj close, prints them; returns dataframe
    2) func -  adds stock returns to a dataframe; returns 'returns dataframe
    3) func - creates correlation DF and writes to excel file; return None
    4) func - call all functions
    
    """


# create dataframe of stocks
def stock_df():
    """aggregates the stocks Adj Close, prints them"""
    data = yf.download(stocks, start='2017-01-01', end='2020-02-15')['Adj Close'].dropna()
    print(data)
    return data


# transform stock returns
def stock_returns(data=None):
    """adds the stocks returns to a dataframe"""
    returns = pd.DataFrame()
    for stocks in data:
        if stocks not in returns:
            returns[stocks] = np.log(data[stocks]).diff()
    returns = returns[1:]
    print(returns)
    return returns


def corr_matrix(df=None):
    """ create correlation matrix & writes to excel file """
    print(df.corr())
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    # to excel
    df.corr().to_excel('El_Chaly_Direxion_3X_correlation.xlsx',sheet_name='Stock_correlation')
    return df.corr()


def stock_corr():
    """calls all functions"""
    data = stock_df()
    df = stock_returns(data=data)
    corr_matrix(df)


# list of stocks to pass through
stocks = ['DFEN', 'NAIL', 'GUSH', 'DUSL',
          'TPOR', 'MIDU', 'EDC', 'RETL', 'DZK', 'CURE', 'UTSL', 'UBOT', 'ZMLP',
          'PILL', 'HIBL', 'TNA', 'DRN', 'FAS', 'TECL', 'SOXL', 'WANT',
          'TAWK', 'NEED', 'WEBL', 'LABU', ]

stock_corr()
