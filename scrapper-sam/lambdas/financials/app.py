import yfinance
import pandas as pd
import json


def handle_get_financials(event, context):
    request_ticker: str = event['queryStringParameters']['ticker']

    ticker = yfinance.Ticker(request_ticker)

    balance_sheet = ticker.balance_sheet.to_dict()

    print(balance_sheet)

    return {
        "statusCode": 200,
        "body": json.dumps(balance_sheet),
        "headers": {
            "Content-Type": "application/json"
        }
    }
