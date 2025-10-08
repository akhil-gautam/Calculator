from pydantic import BaseModel, ConfigDict

class CampaignBase(BaseModel):
    name: str
    description: str | None = None
    budget: float

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    brand_id: int

    model_config = ConfigDict(from_attributes=True)