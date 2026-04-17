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
    # 1. Creates all the tables in the database if they don't exist yet
    Base.metadata.create_all(bind=engine)
    
    # 2. Opens a connection to the database to read/write data
    db = SessionLocal()
    try:
        # 3. We check if we already have users to avoid inserting the same dummy data twice
        user_count = db.query(User).count()
        
        # 4. If users already exist -> do nothing
        if user_count > 0:
            return
            
        # 5. If users do not exist -> insert all dummy data once
        
        # --- Required Users ---
        # Creates our 4 specific test users
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
        # Creates some example clubs
        c1 = Club(club_name="Tech Club", club_description="A place for technology enthusiasts.")
        c2 = Club(club_name="Sports Club", club_description="Stay active and healthy.")
        c3 = Club(club_name="Music Club", club_description="Jam sessions and concerts.")
        
        db.add_all([c1, c2, c3])
        db.commit()
        db.refresh(c1)
        db.refresh(c2)
        db.refresh(c3)
        
        # --- Activities ---
        # Creates example activities and links them to the clubs using club_id
        # Date needs to be python datetime.date
        d1 = datetime.date.today() + datetime.timedelta(days=7)
        t1_start = datetime.time(10, 0)
        t1_end = datetime.time(18, 0)
        
        a1 = Activity(
            activity_title="Hackathon 2026",
            activity_description="24 hour coding challenge to build amazing apps.",
            activity_date=d1,
            start_time=t1_start,
            end_time=t1_end,
            activity_location="FHNW Campus Muttenz",
            max_slots=100,
            activity_category="Technology",
            club_id=c1.club_id
        )
        
        a2 = Activity(
            activity_title="Tennis Tournament",
            activity_description="Annual tennis championship. All levels welcome.",
            activity_date=d1 + datetime.timedelta(days=1),
            start_time=t1_start,
            end_time=t1_end,
            activity_location="Sports Center",
            max_slots=32,
            activity_category="Sports",
            club_id=c2.club_id
        )
        
        a3 = Activity(
            activity_title="AI Workshop",
            activity_description="Learn about the latest trends in Generative AI.",
            activity_date=d1 + datetime.timedelta(days=14),
            start_time=datetime.time(14, 0),
            end_time=datetime.time(16, 0),
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
        # Creates example posts made by our test users
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
        # Shows that a user has joined a specific activity
        ua1 = UserActivity(
            user_id=u1.user_id,
            activity_id=a1.activity_id,
            registration_status="joined"
        )
        db.add(ua1)
        
        # --- Favorites ---
        # Shows users adding clubs and activities to their personal favorites list
        # Add favorite club
        u4.favorite_clubs.append(c1)
        
        # Add favorite activity
        u3.favorite_activities.append(a3)
        
        db.commit()
        
    finally:
        db.close()
