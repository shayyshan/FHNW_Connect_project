# Import Base metadata so Alembic can discover it
from app.models.base import Base

# Import all models here to register them with Base.metadata
from app.models.mixins import TimestampMixin
from app.models.favorites import user_favorite_club, user_favorite_activity
from app.models.user import User
from app.models.club import Club
from app.models.activity import Activity
from app.models.user_activity import UserActivity
from app.models.community_post import CommunityPost
