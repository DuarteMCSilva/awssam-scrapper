import yfinance
import json


def handle_get_financials(event, context):
    request_ticker: str = event['queryStringParameters']['ticker']

    ticker = yfinance.Ticker(request_ticker)

    financials = {
        "ticker": request_ticker,
        "sector": ticker.info['sector'],
        "currency": ticker.fast_info['currency'],
        "marketCap": ticker.fast_info['marketCap'],
        "shares": ticker.fast_info['shares'],
        "beta": ticker.info['beta'],
        "state": getStationaryFinancials(ticker),
        "momentum": getFinancialsByDate(ticker)
    }

    return {
        "statusCode": 200,
        "body": json.dumps(financials),
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:4200',
            'Access-Control-Allow-Methods': 'POST, GET'
        }
    }

def getFinancialsByDate(ticker):
    cash_flow = ticker.cash_flow
    income_statement = ticker.income_stmt

    dates = income_statement.columns.tolist()
    dates.reverse()

    momentum_metrics = []
    data = {}

    for date in dates:
        income_st = income_statement[date]
        cash_flow_st = cash_flow[date]
        format_date = date.strftime('%Y')


        data = {
            "period": format_date,
            "revenue": getValuesWithRelativeChange(income_st.loc['Total Revenue'], data.get('revenue')),
            "grossProfit": getValuesWithRelativeChange(income_st.loc['Gross Profit'], data.get('grossProfit')),
            "netIncome": getValuesWithRelativeChange(income_st.loc['Net Income'], data.get('netIncome')),
            "fcf": getValuesWithRelativeChange(cash_flow_st.loc['Free Cash Flow'], data.get('fcf'))
        }

        momentum_metrics.append(data)
    
    return momentum_metrics

def getValuesWithRelativeChange(value, previous):
    try:
        previous_val = previous.get('value')
        return { "value": value, "change": value/previous_val }
    except:
        return { "value": value }

def getStationaryFinancials(ticker):
    last_balance_sheet = ticker.quarterly_balance_sheet

    current_metrics = {
        "debt": last_balance_sheet.loc['Total Debt'].iloc[0],
        "cash": last_balance_sheet.loc['Cash And Cash Equivalents'].iloc[0],
    }

    return current_metrics
