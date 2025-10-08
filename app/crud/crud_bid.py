from sqlalchemy.orm import Session

from app.models.bid import Bid, BidStatus
from app.schemas.bid import BidCreate


def create_bid(db: Session, bid: BidCreate, influencer_id: int):
    db_bid = Bid(
        amount=bid.amount,
        campaign_id=bid.campaign_id,
        influencer_id=influencer_id,
        status=BidStatus.pending,
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid


def get_bids_for_campaign(db: Session, campaign_id: int):
    return db.query(Bid).filter(Bid.campaign_id == campaign_id).all()


def get_bid(db: Session, id: int):
    return db.query(Bid).filter(Bid.id == id).first()


def update_bid_status(db: Session, db_obj: Bid, status: BidStatus):
    db_obj.status = status
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj