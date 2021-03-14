#!/user/bin/env python
import click

from app import app, models, db, forms
from app.controller import parse_csv as _parse_csv


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, forms=forms)


def _init_db():
    """Utility function to create configured database"""
    db.create_all()


@app.cli.command()
def create_db():
    """Create the configured database with test admin."""
    db.create_all()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


@app.cli.command()
@click.confirmation_option(prompt="Delete all data from database tables?")
def reset_db():
    """Reset the current database."""
    db.drop_all()
    _init_db()


@app.cli.command()
@click.option(
    "-p",
    "--products",
    "model",
    flag_value="products",
    help='Select "PRODUCT" model to import CSV data',
)
@click.option(
    "-r",
    "--reviews",
    "model",
    flag_value="reviews",
    help='Select "REVIEW" model to import CSV data',
)
@click.argument("filename")
def parse_csv(model, filename):
    """Parse CSV files and write to existing db"""
    _parse_csv(model, filename)


if __name__ == "__main__":
    app.run()
