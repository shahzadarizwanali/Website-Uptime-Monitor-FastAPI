from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from typing import Optional
from datetime import datetime, timezone


class Website(SQLModel, table=True):
    __tablename__ = "websites"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(sa_column=Column(String, unique=True, nullable=False))
    name: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    check_interval_sec: int = Field(
        default=60, sa_column=Column(Integer, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, nullable=False),
    )


class WebsiteCheck(SQLModel, table=True):
    __tablename__ = "website_checks"

    id: Optional[int] = Field(default=None, primary_key=True)
    website_id: int = Field(
        sa_column=Column(Integer, ForeignKey("websites.id"), nullable=False)
    )
    checked_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, nullable=False),
    )
    status: str = Field(sa_column=Column(String, nullable=False))
    http_code: Optional[int] = Field(
        default=None, sa_column=Column(Integer, nullable=True)
    )
    response_time_ms: Optional[int] = Field(
        default=None, sa_column=Column(Integer, nullable=True)
    )
    error: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
