from datetime import datetime
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from core.database import SessionLocal
from models import Club, Activity


def get_or_create_club(db, club_name, club_description=None):
    """Get an existing club or create a new one to avoid duplicates."""
    club = db.query(Club).filter(Club.club_name == club_name).first()
    if club:
        return club

    club = Club(
        club_name=club_name,
        club_description=club_description
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


def seed_data():
    """Add sample FHNW clubs and activities to the database."""
    db = SessionLocal()

    try:
        # Create or get all clubs
        clubs = {
            "student_council": get_or_create_club(
                db,
                "Student Council FHNW",
                "Represents FHNW students and organizes social and academic events."
            ),
            "cs_club": get_or_create_club(
                db,
                "Computer Science Club FHNW",
                "A club for students interested in programming, software engineering, AI and cybersecurity."
            ),
            "esn": get_or_create_club(
                db,
                "ESN FHNW",
                "Supports international and exchange students at FHNW."
            ),
            "entrepreneurship": get_or_create_club(
                db,
                "Entrepreneurship Club FHNW",
                "Connects students interested in startups, innovation and business ideas."
            ),
            "sports": get_or_create_club(
                db,
                "FHNW Sports Club",
                "Organizes sports events, tournaments and active student meetups."
            ),
            "sustainability": get_or_create_club(
                db,
                "Sustainability Club FHNW",
                "Promotes sustainability, green innovation and climate awareness."
            ),
            "photography": get_or_create_club(
                db,
                "Photography Club FHNW",
                "A creative student club for photography walks, editing sessions and exhibitions."
            ),
        }

        # Define sample activities
        activities = [
            Activity(
                activity_title="FHNW Welcome BBQ",
                activity_description="Meet new students, enjoy food and network with fellow FHNW students.",
                start_date=datetime(2025, 9, 20, 17, 0),
                end_date=datetime(2025, 9, 20, 21, 0),
                activity_location="Campus Olten Courtyard",
                max_slots=120,
                activity_category="Social",
                image_path="/images/welcome_bbq.jpg",
                club_id=clubs["student_council"].club_id
            ),
            Activity(
                activity_title="Board Game Evening",
                activity_description="Relax with board games, snacks and new friends.",
                start_date=datetime(2025, 9, 22, 19, 0),
                end_date=datetime(2025, 9, 22, 23, 0),
                activity_location="Campus Muttenz Cafeteria",
                max_slots=35,
                activity_category="Social",
                image_path="/images/board_games.jpg",
                club_id=clubs["student_council"].club_id
            ),
            Activity(
                activity_title="AI & Gaming Workshop",
                activity_description="Hands-on workshop exploring AI applications in modern video games.",
                start_date=datetime(2025, 10, 3, 14, 0),
                end_date=datetime(2025, 10, 3, 18, 0),
                activity_location="FHNW Brugg-Windisch Room B204",
                max_slots=40,
                activity_category="Technology",
                image_path="/images/ai_gaming.jpg",
                club_id=clubs["cs_club"].club_id
            ),
            Activity(
                activity_title="Cybersecurity Capture The Flag",
                activity_description="Solve hacking challenges and compete in teams.",
                start_date=datetime(2025, 10, 15, 13, 0),
                end_date=datetime(2025, 10, 15, 19, 0),
                activity_location="FHNW Computer Science Building",
                max_slots=50,
                activity_category="Technology",
                image_path="/images/ctf.jpg",
                club_id=clubs["cs_club"].club_id
            ),
            Activity(
                activity_title="FHNW Coding Night",
                activity_description="Collaborative coding session with pizza and mini challenges.",
                start_date=datetime(2025, 10, 5, 18, 0),
                end_date=datetime(2025, 10, 5, 23, 30),
                activity_location="FHNW Innovation Lab",
                max_slots=70,
                activity_category="Technology",
                image_path="/images/coding_night.jpg",
                club_id=clubs["cs_club"].club_id
            ),
            Activity(
                activity_title="ESN International Meetup",
                activity_description="Exchange students and local students meet for games and networking.",
                start_date=datetime(2025, 9, 28, 18, 30),
                end_date=datetime(2025, 9, 28, 22, 0),
                activity_location="Olten Student Lounge",
                max_slots=80,
                activity_category="Networking",
                image_path="/images/esn_meetup.jpg",
                club_id=clubs["esn"].club_id
            ),
            Activity(
                activity_title="Startup Pitch Night",
                activity_description="Present your startup ideas and receive feedback from mentors.",
                start_date=datetime(2025, 10, 10, 16, 0),
                end_date=datetime(2025, 10, 10, 20, 0),
                activity_location="FHNW Basel Innovation Space",
                max_slots=60,
                activity_category="Business",
                image_path="/images/startup_pitch.jpg",
                club_id=clubs["entrepreneurship"].club_id
            ),
            Activity(
                activity_title="FHNW Football Tournament",
                activity_description="Inter-club football tournament open for all skill levels.",
                start_date=datetime(2025, 9, 25, 10, 0),
                end_date=datetime(2025, 9, 25, 17, 0),
                activity_location="FHNW Sports Field",
                max_slots=100,
                activity_category="Sports",
                image_path="/images/football_tournament.jpg",
                club_id=clubs["sports"].club_id
            ),
            Activity(
                activity_title="Sustainability Week Workshop",
                activity_description="Interactive workshop about sustainable innovation and green tech.",
                start_date=datetime(2025, 10, 8, 15, 0),
                end_date=datetime(2025, 10, 8, 18, 0),
                activity_location="Campus Basel",
                max_slots=45,
                activity_category="Education",
                image_path="/images/sustainability.jpg",
                club_id=clubs["sustainability"].club_id
            ),
            Activity(
                activity_title="Photography Walk Basel",
                activity_description="Explore Basel while improving your photography skills.",
                start_date=datetime(2025, 9, 30, 16, 0),
                end_date=datetime(2025, 9, 30, 19, 0),
                activity_location="Basel City Center",
                max_slots=25,
                activity_category="Creative",
                image_path="/images/photo_walk.jpg",
                club_id=clubs["photography"].club_id
            ),
        ]

        # Add activities, avoiding duplicates
        for activity in activities:
            existing_activity = db.query(Activity).filter(
                Activity.activity_title == activity.activity_title
            ).first()

            if not existing_activity:
                db.add(activity)

        db.commit()
        print("✓ Sample clubs and activities added successfully.")

    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
