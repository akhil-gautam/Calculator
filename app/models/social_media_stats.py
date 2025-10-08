from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class SocialMediaStats(Base):
    __tablename__ = "social_media_stats"

    id = Column(Integer, primary_key=True, index=True)
    influencer_id = Column(Integer, ForeignKey("users.id"))
    likes = Column(Integer)
    comments = Column(Integer)
    engagement = Column(Float)

    influencer = relationship("User", back_populates="social_media_stats")