from sqlalchemy import text

from app.models.base import Base
from app.models.product_intelligence import ProductIntelligence
from tests.fixtures.products import product_catalog


def prepare_database(engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS serving"))
        Base.metadata.create_all(bind=connection)


def seed_products(session) -> None:
    session.query(ProductIntelligence).delete()
    session.add_all(product_catalog())
    session.commit()
