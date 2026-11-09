from enum import StrEnum
from pydantic import BaseModel, ConfigDict


class BaseContract(BaseModel):
    """Base class for all shared contracts."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class Department(StrEnum):
    FINANCIAL = "financial"
    CYBERSECURITY = "cybersecurity"


class TaskStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    FAILED = "failed"


class FindingSeverity(StrEnum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvidenceType(StrEnum):
    DOCUMENT = "document"
    DATABASE_RECORD = "database_record"
    API_RESPONSE = "api_response"
    SECURITY_LOG = "security_log"
    REPORT = "report"
    OTHER = "other"