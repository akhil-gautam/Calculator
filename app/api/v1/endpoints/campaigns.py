from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.user import UserRole

router = APIRouter()


@router.post("/", response_model=schemas.Campaign)
def create_campaign(
    *,
    db: Session = Depends(deps.get_db),
    campaign_in: schemas.CampaignCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create new campaign. Only for users with the 'brand' role.
    """
    if current_user.role != UserRole.brand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    campaign = crud.campaign.create_campaign(
        db=db, campaign=campaign_in, brand_id=current_user.id
    )
    return campaign


@router.get("/", response_model=List[schemas.Campaign])
def read_campaigns(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve campaigns.
    """
    campaigns = crud.campaign.get_campaigns(db, skip=skip, limit=limit)
    return campaigns


@router.get("/{id}", response_model=schemas.Campaign)
def read_campaign(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get campaign by ID.
    """
    campaign = crud.campaign.get_campaign(db, id=id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/{id}", response_model=schemas.Campaign)
def update_campaign(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    campaign_in: schemas.CampaignUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a campaign. Only for users with the 'brand' role who own the campaign.
    """
    campaign = crud.campaign.get_campaign(db, id=id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.brand_id != current_user.id or current_user.role != UserRole.brand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    campaign = crud.campaign.update_campaign(db=db, db_obj=campaign, obj_in=campaign_in)
    return campaign


@router.delete("/{id}", response_model=schemas.Campaign)
def delete_campaign(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Delete a campaign. Only for users with the 'brand' role who own the campaign.
    """
    campaign = crud.campaign.get_campaign(db, id=id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.brand_id != current_user.id or current_user.role != UserRole.brand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    campaign = crud.campaign.delete_campaign(db=db, id=id)
    return campaign