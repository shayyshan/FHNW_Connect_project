from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from app.models.base import Base

# A simple connection table to keep track of which users favorited which clubs (many-to-many)
user_favorite_club = Table(
    'user_favorite_club',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
    Column('club_id', Integer, ForeignKey('clubs.club_id', ondelete='CASCADE'), nullable=False),
    UniqueConstraint('user_id', 'club_id', name='uq_user_club_favorite')
)

# A simple connection table to keep track of which users favorited which activities (many-to-many)
user_favorite_activity = Table(
    'user_favorite_activity',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
    Column('activity_id', Integer, ForeignKey('activities.activity_id', ondelete='CASCADE'), nullable=False),
    UniqueConstraint('user_id', 'activity_id', name='uq_user_activity_favorite')
)
