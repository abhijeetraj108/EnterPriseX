from sqlalchemy import text

from enterprise_x.database.base import Base
from enterprise_x.database.connection import engine

# Import models so SQLAlchemy registers their tables.
from enterprise_x.database import models


SCHEMAS = [
    "platform",
    "financial",
    "cybersecurity",
    "erp",
    "audit",
]


def initialize_database():

    with engine.begin() as connection:

        # Create logical PostgreSQL schemas.
        for schema in SCHEMAS:
            connection.execute(
                text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
            )

        # Create currently registered ORM tables.
        Base.metadata.create_all(bind=connection)

    print("EnterpriseX database initialized successfully.")


if __name__ == "__main__":
    initialize_database()