from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate


def get_campaign(db: Session, id: int):
    return db.query(Campaign).filter(Campaign.id == id).first()


def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Campaign).offset(skip).limit(limit).all()


def create_campaign(db: Session, campaign: CampaignCreate, brand_id: int):
    db_campaign = Campaign(**campaign.model_dump(), brand_id=brand_id)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


def update_campaign(db: Session, *, db_obj: Campaign, obj_in: CampaignUpdate):
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_campaign(db: Session, *, id: int):
    db_obj = db.query(Campaign).get(id)
    db.delete(db_obj)
    db.commit()
    return db_obj