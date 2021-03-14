import csv

from app import db
from app.models import Product, Review
from app.logger import log


def parse_csv(model, filename):
    if model == "products":
        with open(filename, "r") as f:
            csv_reader = csv.DictReader(f)

            # validate CSV file integrity
            if (
                "Asin" not in csv_reader.fieldnames
                or "Title" not in csv_reader.fieldnames
            ):
                log(log.ERROR, "Invalid CSV table structure")
                return

            for row in csv_reader:
                if Product.query.filter_by(asin=row["Asin"]).first():
                    log(log.ERROR, "Product with ASIN: %s already exists", row["Asin"])
                    continue
                product = Product(asin=row["Asin"], title=row["Title"])
                db.session.add(product)
            db.session.commit()
            log(log.INFO, "Products successfully imported")
    elif model == "reviews":
        with open(filename, "r") as f:
            csv_reader = csv.DictReader(f)

            # validate CSV file integrity
            if (
                "Asin" not in csv_reader.fieldnames
                or "Title" not in csv_reader.fieldnames
                or "Review" not in csv_reader.fieldnames
            ):
                log(log.ERROR, "Invalid CSV table structure")
                return

            for row in csv_reader:
                product = Product.query.filter_by(asin=row["Asin"]).first()
                if not product:
                    log(
                        log.ERROR,
                        "No such product with ASIN: %s. Skipping",
                        row["Asin"],
                    )
                    continue
                review = Review(
                    product_id=product._id, title=row["Title"], text=row["Review"]
                )
                db.session.add(review)
            db.session.commit()
            log(log.INFO, "Reviews successfully imported")
    else:
        log(log.ERROR, "Invalid model name: %s already exists", model)
        return
