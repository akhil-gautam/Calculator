from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas, services
from app.api import deps
from app.models.user import UserRole

router = APIRouter()


@router.post("/generate/{influencer_id}", status_code=status.HTTP_201_CREATED)
def generate_social_media_data(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Generate mock social media data for an influencer.
    Can only be triggered by the influencer themselves or a brand.
    """
    user = crud.user.get(db, id=influencer_id)
    if not user or user.role != UserRole.influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")

    if (
        current_user.role != UserRole.brand
        and current_user.id != influencer_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    services.social_media_service.generate_mock_social_media_data(
        db, influencer_id=influencer_id
    )
    return {"message": "Mock social media data generated successfully"}


@router.get("/{influencer_id}", response_model=List[schemas.SocialMediaStats])
def read_social_media_stats(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get social media stats for an influencer.
    """
    user = crud.user.get(db, id=influencer_id)
    if not user or user.role != UserRole.influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")

    stats = crud.social_media_stats.get_social_media_stats_for_influencer(
        db, influencer_id=influencer_id
    )
    return stats


@router.get("/fitness-score/{influencer_id}", response_model=float)
def get_fitness_score(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get the fitness score for an influencer. Only for users with the 'brand' role.
    """
    if current_user.role != UserRole.brand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    user = crud.user.get(db, id=influencer_id)
    if not user or user.role != UserRole.influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")

    stats = crud.social_media_stats.get_social_media_stats_for_influencer(
        db, influencer_id=influencer_id
    )
    score = services.ai_service.calculate_fitness_score(stats)
    return score