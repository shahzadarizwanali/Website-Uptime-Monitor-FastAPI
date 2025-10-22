from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WebsiteCreate(BaseModel):
    url: str
    name: Optional[str] = None
    check_interval_sec: Optional[int] = 60


class WebsiteUpdate(BaseModel):
    url: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    check_interval_sec: Optional[int] = None


class WebsiteCheckRead(BaseModel):
    id: int
    website_id: int
    checked_at: datetime
    status: str
    http_code: Optional[int] = None
    response_time_ms: Optional[int] = None
    error: Optional[str] = None


class WebsiteRead(BaseModel):
    id: int
    url: str
    name: Optional[str]
    is_active: bool
    check_interval_sec: int
    created_at: datetime
    updated_at: datetime
    latest_check: Optional[WebsiteCheckRead] = None
