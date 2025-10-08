from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    budget = Column(Float)
    brand_id = Column(Integer, ForeignKey("users.id"))

    brand = relationship("User", back_populates="campaigns")
    bids = relationship("Bid", back_populates="campaign")