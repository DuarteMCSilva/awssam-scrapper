# Project Broker

## Elements
- Angular Frontend
- Spring Boot or Quarkus Backend
- AWS Lambdas for scrappers
- Database

### Frontend

The frontend needs to get:
Portfolio page
- GET current snapshot
- GET portfolio Evolution

Upload page:
- POST transactions file

### Quarkus
- Get current snapshot from database ?? Calculate from Transactions (where should it be calculated?) ?? Empty
- Get portfolio evolution from database ?? Request histories (if transactions) and calculate evolution ?? Empty

- Save transactions file to database & Calculate portfolio snapshots and save to DB & Calculate evolution and save to DB

### DB

#### Snapshots

INITIAL IMPLEMENTATION:
DATE | QT.SNAPSHOT | VALUE

where QT.SNAPSHOT values are strings with the following format: "PYPL:4;AAPL:3;ALTR.LS:20"

Long term implementation:
1. Portfolio Table (Metadata about portfolio on a specific day)

| Column      | Data Type | Description                              |
|-------------|------------|------------------------------------------|
| `id`        | INT        | Primary key, unique identifier           |
| `date`      | DATE       | The date of the portfolio snapshot       |
| `total_value` | DECIMAL  | Total portfolio value on this date       |

2. Holdings Table (Only records changes in the number of shares held)

| Column        | Data Type | Description                                    |
|---------------|------------|-----------------------------------------------|
| `id`          | INT        | Primary key, unique identifier for each holding |
| `portfolio_id` | INT       | Foreign key referencing the `Portfolio` table |
| `ticker`      | VARCHAR    | Stock ticker symbol (e.g., "AAPL")            |
| `quantity`    | DECIMAL    | Number of shares held                         |
| `last_updated` | DATE      | The last date when the holdings were changed  |

The Holdings Table stores each stock's ticker and the quantity held, but only when there's a change in the portfolio (buy/sell). last_updated helps identify when the holdings for a particular stock were last modified.

3. Prices Table (Stores daily stock prices for each ticker)

| Column  | Data Type | Description                            |
|---------|------------|----------------------------------------|
| `id`    | INT        | Primary key, unique identifier         |
| `ticker`| VARCHAR    | Stock ticker symbol (e.g., "AAPL")     |
| `date`  | DATE       | Date of the stock price                |
| `price` | DECIMAL    | Stock price on this date               |

This table keeps track of daily stock prices for each ticker. Each stock will have one row per day, allowing you to reference the price for calculating the total portfolio value for any given date.

### AWS Lambda
 - getHistoricalPrices(ticker[]): should accept list of tickers and should send back response of type { ticker: string, hist: { date: value}[] }[]
 - getFinancialData -> SOON

## Next Steps:

- Choose a database (PostgreSQL recommended) -> Make it DOCKER containerized
- Set up a Spring Boot project using Spring Initializr.
- Configure database credentials and connection in application.properties.
- Create entities and repositories for Portfolio, Holdings, and Prices tables.
- Implement business logic to calculate portfolio value using daily stock prices.
- Optionally, schedule price synchronization using external APIs.
