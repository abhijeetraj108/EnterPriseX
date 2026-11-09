import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enterprise_x.database.base import Base, TimestampMixin


class Investigation(Base, TimestampMixin):

    __tablename__ = "investigations"
    __table_args__ = (
        Index("ix_investigations_tenant_status", "tenant_id", "status"),
        {"schema": "platform"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(40),
        default="created",
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="medium",
        nullable=False
    )

    created_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    
    tasks: Mapped[list["InvestigationTask"]] = relationship(
        back_populates="investigation"
    )

class InvestigationTask(Base, TimestampMixin):

    __tablename__ = "investigation_tasks"
    __table_args__ = (
        Index("ix_tasks_investigation_status", "investigation_id", "status"),
        {"schema": "platform"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("platform.investigations.id"),
        nullable=False
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )

    task_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    objective: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(40),
        default="pending",
        nullable=False
    )

    input_context: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False
    )

    result_ref: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    investigation: Mapped["Investigation"] = relationship(
        back_populates="tasks"
    )