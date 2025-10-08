from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()


@router.post("/", response_model=schemas.Bid)
def create_bid(
    *,
    db: Session = Depends(deps.get_db),
    bid_in: schemas.BidCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create new bid. Only for users with the 'influencer' role.
    """
    if current_user.role != UserRole.influencer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    campaign = crud.campaign.get_campaign(db, id=bid_in.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    bid = crud.bid.create_bid(db=db, bid=bid_in, influencer_id=current_user.id)
    return bid


@router.get("/campaign/{campaign_id}", response_model=List[schemas.Bid])
def read_bids_for_campaign(
    *,
    db: Session = Depends(deps.get_db),
    campaign_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get all bids for a campaign. Only for the brand that owns the campaign.
    """
    campaign = crud.campaign.get_campaign(db, id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.brand_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    bids = crud.bid.get_bids_for_campaign(db, campaign_id=campaign_id)
    return bids


@router.put("/{id}/status", response_model=schemas.Bid)
def update_bid_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    bid_in: schemas.BidUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update the status of a bid. Only for the brand that owns the campaign.
    """
    bid = crud.bid.get_bid(db, id=id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    campaign = crud.campaign.get_campaign(db, id=bid.campaign_id)
    if campaign.brand_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    bid = crud.bid.update_bid_status(db=db, db_obj=bid, status=bid_in.status)
    return bid