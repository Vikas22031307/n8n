from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import get_db, Base, engine
from .crud import list_workflows
from . import models
from .schemas import WorkflowOut
from typing import List, Optional

Base.metadata.create_all(bind=engine)
app = FastAPI(title="n8n Workflow Popularity API (human)")

def build_popularity_dict(row: models.Workflow) -> dict:
    metrics = {
        "views": row.views,
        "likes": row.likes,
        "comments": row.comments,
        "like_to_view_ratio": row.like_to_view_ratio,
        "comment_to_view_ratio": row.comment_to_view_ratio
    }
    if row.replies is not None:
        metrics["replies"] = row.replies
    if row.unique_contributors is not None:
        metrics["unique_contributors"] = row.unique_contributors
    if row.monthly_search_volume is not None:
        metrics["monthly_search_volume"] = row.monthly_search_volume
    if row.change_last_60_days is not None:
        metrics["change_last_60_days"] = row.change_last_60_days
    metrics = {k: v for k, v in metrics.items() if v is not None}
    return metrics

@app.get('/workflows', response_model=List[WorkflowOut])
def get_workflows(
    platform: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    rows = list_workflows(db, platform=platform, country=country, limit=limit, offset=offset)
    out = []
    for r in rows:
        out.append({
            "workflow": r.workflow,
            "platform": r.platform,
            "country": r.country,
            "popularity_metrics": build_popularity_dict(r)
        })
    return out

@app.get('/health')
def health():
    return {'status': 'ok'}
