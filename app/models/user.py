from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class UserRole(str, enum.Enum):
    influencer = "influencer"
    brand = "brand"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(UserRole))

    campaigns = relationship("Campaign", back_populates="brand")
    bids = relationship("Bid", back_populates="influencer")
    social_media_stats = relationship("SocialMediaStats", back_populates="influencer")