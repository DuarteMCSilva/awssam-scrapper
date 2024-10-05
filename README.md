# Project Broker

## Elements
- Angular Frontend
- Spring Boot or Quarkus Backend
- AWS Lambdas for scrappers
- Database

## Frontend

The frontend needs to get:
Portfolio page
- GET current snapshot
- GET portfolio Evolution

Upload page:
- POST transactions file

## Quarkus
- Get current snapshot from database ?? Calculate from Transactions (where should it be calculated?) ?? Empty
- Get portfolio evolution from database ?? Request histories (if transactions) and calculate evolution ?? Empty

- Save transactions file to database & Calculate portfolio snapshots and save to DB & Calculate evolution and save to DB

## DB

### Snapshots
DATE | QT.SNAPSHOT | VALUE

where QT.SNAPSHOT values are strings with the following format: "PYPL:4;AAPL:3;ALTR.LS:20"

## AWS Lambda
 - getHistoricalPrices(ticker[]): should accept list of tickers and should send back response of type { ticker: string, hist: { date: value}[] }[]
 - getFinancialData -> SOON
