from sqlalchemy.orm import Session

from app.models.social_media_stats import SocialMediaStats
from app.schemas.social_media_stats import SocialMediaStatsCreate


def create_social_media_stats(db: Session, stats: SocialMediaStatsCreate):
    db_stats = SocialMediaStats(
        likes=stats.likes,
        comments=stats.comments,
        engagement=stats.engagement,
        influencer_id=stats.influencer_id,
    )
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats


def get_social_media_stats_for_influencer(db: Session, influencer_id: int):
    return (
        db.query(SocialMediaStats)
        .filter(SocialMediaStats.influencer_id == influencer_id)
        .all()
    )