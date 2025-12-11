from sqlalchemy.orm import Session
from . import models
from typing import Dict

def normalize_keyset(row: Dict) -> Dict:
    allowed = {
        "workflow", "platform", "country",
        "views", "likes", "comments",
        "like_to_view_ratio", "comment_to_view_ratio",
        "replies", "unique_contributors",
        "monthly_search_volume", "change_last_60_days",
        "extra"
    }
    return {k: v for k, v in row.items() if k in allowed}

def upsert_workflow(db: Session, wf_data: Dict):
    wf_data = normalize_keyset(wf_data)
    existing = db.query(models.Workflow).filter(
        models.Workflow.workflow == wf_data["workflow"],
        models.Workflow.platform == wf_data["platform"],
        models.Workflow.country == wf_data["country"]
    ).first()

    if existing:
        for k, v in wf_data.items():
            setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return existing

    new_wf = models.Workflow(**wf_data)
    db.add(new_wf)
    db.commit()
    db.refresh(new_wf)
    return new_wf

def list_workflows(db: Session, platform: str = None, country: str = None, limit: int = 100, offset: int = 0):
    q = db.query(models.Workflow)
    if platform:
        q = q.filter(models.Workflow.platform == platform)
    if country:
        q = q.filter(models.Workflow.country == country)
    q = q.order_by(models.Workflow.views.desc().nullslast())
    return q.offset(offset).limit(limit).all()
