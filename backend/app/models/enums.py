import enum


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCategory(str, enum.Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    ACCOUNT = "account"
    FEATURE_REQUEST = "feature_request"
    GENERAL = "general"
