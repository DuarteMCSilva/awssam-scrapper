import yfinance
import pandas as pd


def handle_get_prices_request(event, context):
    request_ticker: str = 'AAPL' #request.GET.get('ticker')
    period: str = '1y' # request.GET.get('p')
    interval: str = '1mo'

    historical_prices = process_historical_prices_by_date(request_ticker, period, interval)

    close_prices = historical_prices.set_index('Date')['Close'].to_dict()

    return close_prices

def process_historical_prices_by_date(ticker, period, interval):
    history_df = fetch_historical_prices_from_api(ticker, period, interval)

    if history_df.index.name == 'Date':
        history_df = history_df.reset_index()
    history_df['Date'] = pd.to_datetime(history_df['Date'])
    history_df['Date'] = history_df['Date'].dt.strftime('%Y%m%d')
    return history_df

def fetch_historical_prices_from_api(ticker: str = None, period_input: str = '', interval: str = '1mo'):
    if ticker is None:
        return 'No ticker provided!'

    period = choose_valid_period(period_input)

    ticker = yfinance.Ticker(ticker)
    return ticker.history(period=period, interval=interval)

def choose_valid_period(period_input: str = ''):
    possible_vals = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    if period_input not in possible_vals:
        period = '5y'
    else:
        period = period_input

    return period
