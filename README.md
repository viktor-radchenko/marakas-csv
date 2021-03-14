# Marakas-CSV

Simple Flask application using SQLite for development and Postgres for production. 
### How to run project locally:
1. Clone this repo

2. Create and activate virtual environment:
	(for Mac) `python3 -m virtualenv .venv && . .venv/bin/activate`

3.  Install project dependencies:
	`pip install -r requirements.txt`

4. Unzip .env file:
	`unzip env.zip` (password: marakas)

5. Create database:
	`flask create-db`

6. Import `products.csv` and `reviews.csv`:
	`flask parse-csv -p products.csv`
	`flask parse-csv -r reviews.csv`
	NOTE: if you try importing reviews before products you will recieve an error:
	`[ERROR   ] No such product with ASIN: B06XYPJN4G. Skipping`

7. Run application:
	`flask run`

You can check application endpoints using command: `flask routes`
This application is covered by tests. To test application use command `pytest`
