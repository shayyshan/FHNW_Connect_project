import datetime
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.base import Base

# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.club import Club
from app.models.activity import Activity
from app.models.user_activity import UserActivity
from app.models.community_post import CommunityPost
from app.models.favorites import user_favorite_club, user_favorite_activity

# This function sets up the database tables and inserts dummy data for testing
def init_db():
    # Recreate the schema and seed with the same dummy data on each startup
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # --- Required Users ---
        u1 = User(email="shannon.polak@students.fhnw.ch", username="shannonpolak", password_hash="1234")
        u2 = User(email="katrin.schuette@students.fhnw.ch", username="katrinschuette", password_hash="1234")
        u3 = User(email="alondramaria.diaznavarro@students.fhnw.ch", username="alondradiaz", password_hash="1234")
        u4 = User(email="jorge.mera@students.fhnw.ch", username="jorgemera", password_hash="1234")

        db.add_all([u1, u2, u3, u4])
        db.commit()
        db.refresh(u1)
        db.refresh(u2)
        db.refresh(u3)
        db.refresh(u4)

        # --- Clubs ---
        c1 = Club(club_name="Tech Club", club_description="A place for technology enthusiasts.")
        c2 = Club(club_name="Sports Club", club_description="Stay active and healthy.")
        c3 = Club(club_name="Music Club", club_description="Jam sessions and concerts.")

        db.add_all([c1, c2, c3])
        db.commit()
        db.refresh(c1)
        db.refresh(c2)
        db.refresh(c3)

        # --- Activities ---
        d1 = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=7), datetime.time(10, 0))
        a1 = Activity(
            activity_title="Hackathon 2026",
            activity_description="24 hour coding challenge to build amazing apps.",
            start_date=d1,
            end_date=d1.replace(hour=18),
            activity_location="FHNW Campus Muttenz",
            max_slots=100,
            activity_category="Technology",
            club_id=c1.club_id
        )

        d2 = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=8), datetime.time(10, 0))
        a2 = Activity(
            activity_title="Tennis Tournament",
            activity_description="Annual tennis championship. All levels welcome.",
            start_date=d2,
            end_date=d2.replace(hour=18),
            activity_location="Sports Center",
            max_slots=32,
            activity_category="Sports",
            club_id=c2.club_id
        )

        d3 = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=21), datetime.time(14, 0))
        a3 = Activity(
            activity_title="AI Workshop",
            activity_description="Learn about the latest trends in Generative AI.",
            start_date=d3,
            end_date=d3.replace(hour=16),
            activity_location="Room 101",
            max_slots=50,
            activity_category="Technology",
            club_id=c1.club_id
        )

        db.add_all([a1, a2, a3])
        db.commit()
        db.refresh(a1)
        db.refresh(a2)
        db.refresh(a3)

        # --- Community Posts ---
        p1 = CommunityPost(
            community_post_title="Looking for a Hackathon team",
            community_post_description="I'm a backend developer looking for frontend and design folks. Hit me up!",
            community_post_category="Looking for team",
            user_id=u1.user_id,
            club_id=c1.club_id
        )

        p2 = CommunityPost(
            community_post_title="Tennis partner wanted",
            community_post_description="Looking for someone to practice with before the tournament this weekend.",
            community_post_category="Sports",
            user_id=u2.user_id,
            club_id=c2.club_id
        )

        p3 = CommunityPost(
            community_post_title="Welcome to FHNW Connect",
            community_post_description="Check out the new features of our platform! Let's connect.",
            community_post_category="Announcements",
            user_id=u3.user_id,
            club_id=None
        )

        db.add_all([p1, p2, p3])

        # --- UserActivity (participation) ---
        ua1 = UserActivity(
            user_id=u1.user_id,
            activity_id=a1.activity_id,
            registration_status="joined"
        )
        db.add(ua1)

        # --- Favorites ---
        u4.favorite_clubs.append(c1)
        u3.favorite_activities.append(a3)

        db.commit()

    finally:
        db.close()
