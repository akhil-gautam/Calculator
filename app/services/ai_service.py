from typing import List
from app.models.social_media_stats import SocialMediaStats

def calculate_fitness_score(stats: List[SocialMediaStats]) -> float:
    """
    Calculates a fitness score for an influencer based on their social media stats.
    This is a simple placeholder implementation.
    """
    if not stats:
        return 0.0

    total_engagement = sum(s.engagement for s in stats)
    avg_engagement = total_engagement / len(stats)

    # Simple scoring logic: score is based on average engagement rate.
    # A more sophisticated model would consider likes, comments, campaign goals, etc.
    score = min(avg_engagement * 10, 100)  # Scale to 0-100

    return round(score, 2)