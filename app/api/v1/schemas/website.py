from pydantic import BaseModel
from typing import Optional


class WebsiteCreate(BaseModel):
    url: str
    name: Optional[str] = None
    check_interval_sec: Optional[int] = 60


class WebsiteUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    check_interval_sec: Optional[int] = None
