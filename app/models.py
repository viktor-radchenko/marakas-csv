from . import db


class ModelMixin(object):
    """Utility class to facilitate saving database objects"""

    def save(self):
        # Save this model to the database.
        db.session.add(self)
        db.session.commit()
        return self


class Product(db.Model, ModelMixin):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    asin = db.Column(db.String(16), unique=True, nullable=False)
    reviews = db.relationship("Review", backref=db.backref("product", lazy=True))

    def to_json(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Product {self._id}>"


class Review(db.Model, ModelMixin):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    text = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product._id"), nullable=False)

    def to_json(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Review {self._id}>"
