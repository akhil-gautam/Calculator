import random
from sqlalchemy.orm import Session

from app import crud, schemas


def generate_mock_social_media_data(db: Session, influencer_id: int):
    """
    Generates mock social media data for an influencer for the last 10 posts.
    """
    for _ in range(10):
        likes = random.randint(100, 10000)
        comments = random.randint(10, 1000)
        engagement = round(random.uniform(0.5, 10.0), 2)
        stats_in = schemas.SocialMediaStatsCreate(
            likes=likes,
            comments=comments,
            engagement=engagement,
            influencer_id=influencer_id,
        )
        crud.social_media_stats.create_social_media_stats(db, stats=stats_in)