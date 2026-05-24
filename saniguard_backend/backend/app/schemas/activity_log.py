from datetime import datetime
from pydantic import BaseModel
from app.domain.activity_log import ActivityType


class ActivityLogOut(BaseModel):
    id: str
    action: str
    username: str
    role: str
    type: ActivityType
    created_at: datetime
