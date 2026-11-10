from sqlalchemy import Engine, text

from enterprise_x.database.base import Base
from enterprise_x.database.connection import engine
from enterprise_x.database.models.erp import (
    ERPInvoice,
    ERPPurchaseOrder,
    ERPVendor,
)

ERP_TABLES = [
    ERPVendor.__table__,
    ERPPurchaseOrder.__table__,
    ERPInvoice.__table__,
]


def initialize_database(database_engine: Engine) -> None:
    if database_engine.dialect.name == "sqlite":
        database_engine = database_engine.execution_options(
            schema_translate_map={"erp": None}
        )
    with database_engine.begin() as connection:
        if database_engine.dialect.name != "sqlite":
            connection.execute(text('CREATE SCHEMA IF NOT EXISTS "erp"'))
        Base.metadata.create_all(bind=connection, tables=ERP_TABLES)
        if database_engine.dialect.name == "postgresql":
            connection.execute(
                text(
                    "ALTER TABLE erp.vendors "
                    "ADD COLUMN IF NOT EXISTS bank_account_changed_at "
                    "TIMESTAMPTZ"
                )
            )
