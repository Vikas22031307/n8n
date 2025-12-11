from pydantic import BaseModel
from typing import Optional, Any

class PopularityMetrics(BaseModel):
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    like_to_view_ratio: Optional[float] = None
    comment_to_view_ratio: Optional[float] = None

    replies: Optional[int] = None
    unique_contributors: Optional[int] = None

    monthly_search_volume: Optional[int] = None
    change_last_60_days: Optional[float] = None

class WorkflowOut(BaseModel):
    workflow: str
    platform: str
    popularity_metrics: PopularityMetrics
    country: str
