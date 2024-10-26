import yfinance
import pandas as pd
import json


def handle_get_financials(event, context):
    request_ticker: str = event['queryStringParameters']['ticker']

    ticker = yfinance.Ticker(request_ticker)

    financials = {
        "ticker": request_ticker,
        "currency": ticker.fast_info['currency'],
        "marketCap": ticker.fast_info['marketCap'],
        "shares": ticker.fast_info['shares'],
        "beta": ticker.info['beta'],
        "state": getStationaryFinancials(ticker),
        "momentum": getFinancialsByDate(ticker)
    }

    return {
        "statusCode": 200,
        "body": financials,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:4200',
            'Access-Control-Allow-Methods': 'POST, GET'
        }
    }

def getFinancialsByDate(ticker):
    cash_flow = ticker.cash_flow
    income_statement = ticker.income_stmt

    dates = income_statement.columns

    momentum_metrics = {}

    for date in dates:
        income_st = income_statement[date]
        cash_flow_st = cash_flow[date]

        data = {
            "revenue": income_st.loc['Total Revenue'],
            "grossProfit": income_st.loc['Gross Profit'],
            "netIncome": income_st.loc['Gross Profit'],
            "fcf": cash_flow_st.loc['Free Cash Flow']
        }

        format_date = date.strftime('%Y')
        momentum_metrics[format_date] = data
    
    return momentum_metrics

def getStationaryFinancials(ticker):
    last_balance_sheet = ticker.quarterly_balance_sheet

    current_metrics = {
        "debt": last_balance_sheet.loc['Total Debt'].iloc[0],
        "cash": last_balance_sheet.loc['Cash And Cash Equivalents'].iloc[0],
    }

    return current_metrics
