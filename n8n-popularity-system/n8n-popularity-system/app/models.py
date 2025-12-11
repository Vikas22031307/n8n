from sqlalchemy import Column, Integer, String, Float, JSON
from .database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow = Column(String, index=True, nullable=False)
    platform = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)

    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    like_to_view_ratio = Column(Float, nullable=True)
    comment_to_view_ratio = Column(Float, nullable=True)

    replies = Column(Integer, nullable=True)
    unique_contributors = Column(Integer, nullable=True)

    monthly_search_volume = Column(Integer, nullable=True)
    change_last_60_days = Column(Float, nullable=True)

    extra = Column(JSON, nullable=True)
