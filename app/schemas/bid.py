from pydantic import BaseModel, ConfigDict
from app.models.bid import BidStatus

class BidBase(BaseModel):
    amount: float

class BidCreate(BidBase):
    campaign_id: int

class BidUpdate(BaseModel):
    status: BidStatus

class Bid(BidBase):
    id: int
    influencer_id: int
    campaign_id: int
    status: BidStatus

    model_config = ConfigDict(from_attributes=True)