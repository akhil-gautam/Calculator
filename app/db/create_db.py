from app.db.database import Base, engine
from app.models.user import User
from app.models.campaign import Campaign
from app.models.bid import Bid
from app.models.social_media_stats import SocialMediaStats

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")