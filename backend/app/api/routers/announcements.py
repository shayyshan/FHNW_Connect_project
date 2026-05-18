from fastapi import APIRouter

router = APIRouter()

@router.get("/announcements")
def get_announcements():
    return [{"id": 1, "title": "Welcome Event", "description": "Don't miss our kickoff event!"}]

# TODO: Implement database connection and model for announcements, similar to activities and clubs.