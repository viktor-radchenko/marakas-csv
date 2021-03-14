import os
from io import TextIOWrapper

from app import app, db
from app.models import Product, Review
from app.controller import parse_csv
from .fixtures import client

from .utils import (
    create_invalid_product_csv,
    create_review_csv,
    create_invalid_review_csv,
    create_product_data
)


def test_csv_parser(client):
    """Validate proper csv files could be imported"""

    filename = "test_products.csv"
    products = Product.query.all()
    assert not products

    create_product_data(filename)
    products = Product.query.all()

    # Check if all 5 products were imported
    assert len(products) == 5
    assert products[0].asin == "ABCDE00001"

    # Check there are no duplicates with same ASIN
    create_product_data(filename)
    products = Product.query.all()
    assert len(products) == 5

    # Clean up temp files
    os.remove(filename)

    # Check reviews are imported properly
    create_review_csv()
    filename = "test_reviews.csv"
    reviews = Review.query.all()
    assert not reviews

    parse_csv("reviews", filename)
    product = Product.query.first()
    assert len(product.reviews) == 5

    # Clean up temp files
    os.remove(filename)


def test_invalid_product_csv_parser(client):
    """Validate malformed csv files could not be imported"""

    create_invalid_product_csv()
    filename = "test_invalid_products.csv"
    products = Product.query.all()
    assert not products

    parse_csv("products", filename)
    products = Product.query.all()

    # Check none of products were imported
    assert not products
    # Clean up temp files
    os.remove(filename)


def test_invalid_review(client):
    """Validate malformed reviews csv could not be imported as well as reviews without existing product id"""

    create_review_csv()
    filename = "test_reviews.csv"
    parse_csv("reviews", filename)
    reviews = Review.query.all()
    assert not reviews
    
    # Clean up temp files
    os.remove(filename)