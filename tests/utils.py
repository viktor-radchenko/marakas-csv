import csv

from app.controller import parse_csv


product_data = [
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1",
    },
    {
        "Asin": "ABCDE00002",
        "Title": "Test product #2",
    },
    {
        "Asin": "ABCDE00003",
        "Title": "Test product #3",
    },
    {
        "Asin": "ABCDE00004",
        "Title": "Test product #4",
    },
    {
        "Asin": "ABCDE00005",
        "Title": "Test product #5",
    },
]

invalid_product_data = [
    {
        "Nisa": "ABCDE00001",
        "Eltit": "Test product #1",
    },
    {
        "Nisa": "ABCDE00002",
        "Eltit": "Test product #2",
    },
]

review_data = [
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #1",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #2",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #3",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #4",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #5",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00002",
        "Title": "Test product #2 review",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00003",
        "Title": "Test product #3 review",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00004",
        "Title": "Test product #4 review",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
    {
        "Asin": "ABCDE00005",
        "Title": "Test product #5 review",
        "Review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    },
]

invalid_review_data = [
    {
        "Asin": "ABCDE00001",
        "Title": "Test product #1 review #1",
        "Text": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
    }
]

put_review_data = {
    "title": "Very nice product indeed",
    "review": "Lorem ipsum dolor sit amet consecture ametir evanus dole id campus",
}


def create_products_csv():
    """Create temp csv file with products data"""
    filename = "test_products.csv"
    columns = ["Asin", "Title"]
    with open(filename, "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=columns)
        csv_writer.writeheader()
        for row in product_data:
            csv_writer.writerow(row)


def create_invalid_product_csv():
    """Create temp products csv to test against file integrity"""
    filename = "test_invalid_products.csv"
    columns = ["Nisa", "Eltit"]
    with open(filename, "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=columns)
        csv_writer.writeheader()
        for row in invalid_product_data:
            csv_writer.writerow(row)


def create_review_csv():
    """Create temp csv file with review data"""
    filename = "test_reviews.csv"
    columns = ["Asin", "Title", "Review"]
    with open(filename, "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=columns)
        csv_writer.writeheader()
        for row in review_data:
            csv_writer.writerow(row)


def create_invalid_review_csv():
    """Create temp products csv to test against file integrity"""
    filename = "test_invalid_reviews.csv"
    columns = ["Asin", "Title", "Text"]
    with open(filename, "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=columns)
        csv_writer.writeheader()
        for row in invalid_review_data:
            csv_writer.writerow(row)


def create_product_data(filename):
    create_products_csv()
    parse_csv("products", filename)
