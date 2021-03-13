import pytest

from app import app, db


@pytest.fixture
def client():
    """Basic pytest fixture for Flask test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()
