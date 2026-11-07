from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from langchain_aws import ChatBedRockConverse

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseContract(BaseModel):
    """
    Base class for all EnterpriseX shared contracts.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )


class Severity(str, Enum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EntityReference(BaseContract):
    """
    Reference to an enterprise entity without copying
    its complete database record.
    """

    entity_type: str
    entity_id: str
    display_name: str | None = None


class ContractMetadata(BaseContract):
    """
    Metadata common to versioned contracts.
    """

    schema_version: str = "1.0"
    created_at: datetime = Field(default_factory=utc_now)