import os

from app import cache
from app.controller import parse_csv
from app.models import Product
from .fixtures import client as test_client
from .utils import create_product_data, put_review_data, create_review_csv


client = test_client


def test_endpoints(client):
    """Basic validation of endpoints integrity"""

    res = client.get("/api/products/")
    assert res.status_code == 200

    filename = "test_products.csv"
    create_product_data(filename)
    assert len(Product.query.all()) == 5

    # Clear cache to overcome 60s cache timeout
    cache.clear()
    res = client.get("/api/products/")
    assert len(res.json["products"]) == 5
    assert b"ABCDE00001" in res.data

    res = client.get("/api/products/1")
    assert res.status_code == 200

    # Check PUT endpoint for review exists and handles empty data
    res = client.put("/api/products/1")
    assert res.status_code == 400

    # Clean up temp data
    os.remove(filename)


def test_get_product_details(client):
    filename = "test_products.csv"
    create_product_data(filename)
    # Clean up temp data
    os.remove(filename)

    filename = "test_reviews.csv"
    create_review_csv()
    parse_csv("reviews", filename)

    # Check pagination links are present in response data
    res = client.get("/api/products/1?page=2&per_page=1")
    res_json = res.get_json()
    assert res_json.get("next_url")
    assert res_json.get("prev_url")

    # Clean up temp data
    os.remove(filename)


def test_adding_new_review(client):
    api = "/api/products/1"
    filename = "test_products.csv"
    create_product_data(filename)

    # Check valid review data is processed properly
    res = client.put(api, json=put_review_data)
    assert res.status_code == 201
    assert b"Lorem ipsum" in res.data

    # Check invalid data returns 400
    res = client.put(
        api,
        json={
            "invalid_title": "Test invalid review title",
            "invalid_review": "Test invalid review text",
        },
    )
    assert res.status_code == 400
    assert b"Review data is not valid" in res.data

    # Check reviews could not be added for non existing product
    # Check invalid data returns 400
    res = client.put(
        "/api/products/101",
        json=put_review_data,
    )
    assert res.status_code == 400
    assert b"Product does not exist" in res.data

    # Clean up temp data
    os.remove(filename)
