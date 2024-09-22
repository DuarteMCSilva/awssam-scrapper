import json
import yfinance
import pandas as pd


def lambda_handler(event, context):
    request_ticker: str = 'AAPL'#request.GET.get('ticker')
    period: str = '1d' # request.GET.get('p')

    history_df = get_historical_prices(request_ticker, period)

    print(history_df)

    if history_df.index.name == 'Date':
        history_df = history_df.reset_index()
    history_df['Date'] = pd.to_datetime(history_df['Date'])
    history_df['Date'] = history_df['Date'].dt.strftime('%Y%m%d')

    key_value_map = history_df.set_index('Date')['Close'].to_dict()

    json_response = key_value_map#json.dumps(key_value_map, indent=4)

    return json_response #json.dumps(json_response, safe=False)

def get_historical_prices(ticker: str = None, period: str = ''):

    possibleVals = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    if ticker == None: 
        return HttpResponse('No ticker provided!')
    
    if period not in possibleVals:
        period = "5y"

    ticker = yfinance.Ticker(ticker)
    return ticker.history(period=period, interval= '1mo')