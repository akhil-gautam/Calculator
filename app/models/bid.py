from sqlalchemy import Column, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class BidStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    influencer_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    status = Column(Enum(BidStatus), default=BidStatus.pending)

    influencer = relationship("User", back_populates="bids")
    campaign = relationship("Campaign", back_populates="bids")