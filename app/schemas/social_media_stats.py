from pydantic import BaseModel, ConfigDict

class SocialMediaStatsBase(BaseModel):
    likes: int
    comments: int
    engagement: float

class SocialMediaStatsCreate(SocialMediaStatsBase):
    influencer_id: int

class SocialMediaStats(SocialMediaStatsBase):
    id: int
    influencer_id: int

    model_config = ConfigDict(from_attributes=True)