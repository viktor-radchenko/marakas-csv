from flask import render_template, jsonify, request, url_for

from app import app, cache
from .models import Product, Review
from app.logger import log


# Normally blueprints are used and views are defined in a seperate module. Routes are put in one file for simplicity
@app.route("/api/products/")
@cache.cached(timeout=60)
def get_products():
    products = Product.query.all()
    products_list = [product.to_json() for product in products]
    return jsonify({"products": products_list})


@app.route("/api/products/<int:product_id>")
@cache.cached(timeout=60)
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if not product:
        log(log.ERROR, "Product with id %d does not exist", product_id)
        return jsonify({"error": "Product does not exist"}), 400
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=1, type=int)
    reviews = Review.query.filter_by(product_id=product_id).paginate(
        page, per_page, False
    )
    review_paginated = [review.to_json() for review in reviews.items]
    next_url = (
        url_for("get_product_details", product_id=product_id, page=reviews.next_num, _external=True)
        if reviews.has_next
        else None
    )
    prev_url = (
        url_for("get_product_details", product_id=product_id, page=reviews.prev_num, _external=True)
        if reviews.has_prev
        else None
    )
    res = {"product": product.to_json(),'reviews': review_paginated, "next_url": next_url, "prev_url": prev_url}
    return jsonify(res)


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def add_review(product_id):
    product = Product.query.get(product_id)
    if not product:
        log(log.ERROR, "Product with id %d does not exist", product_id)
        return jsonify({"error": "Product does not exist"}), 400
    request_json = request.get_json()
    if not request_json:
        log(log.ERROR, "No review details provided")
        return jsonify({"error": "No review details provided"}), 400
    if not request_json.get('title') or not request_json.get('review'):
        log(log.ERROR, "Review data is not valid")
        return jsonify({"error": "Review data is not valid"}), 400
    review = Review(
        title=request_json["title"],
        text=request_json["review"],
        product_id=product_id,
    )
    review.save()
    log(log.INFO, "Review successfully added for product %d", product_id)
    return jsonify({"review": review.to_json()}), 201
