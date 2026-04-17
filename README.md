# FHNW_Connect_project
FHNW - Internet Technology Project - Brugg 2

# FHNWConnect

## Part 1: Analysis

### Scenario
FHNWConnect is a university event platform that helps students discover what is happening on campus. It centralizes activities from student clubs and sports into one platform. 

Students can browse upcoming activities, search and filter them, mark favorites, and join or leave activities. Clubs can organize activities, publish announcements, and monitor participation.

---

### User Stories

- As a Student, I want to browse all campus activities so that I can find interesting things to do.
- As a Student, I want to search and filter activities by category, date, club, and location so that I can quickly find relevant activities.
- As a Student, I want to favorite clubs and activities so that I get a more personalized experience.
- As a Student, I want to join or leave activities so that I can manage my participation.
- As a Club, I want to create activities so that students can join them.
- As a Club, I want to post announcements so that I can inform students about updates or changes.
- As a Club, I want to view participation numbers so that I can better plan my activities.
- As a User, I want to access the platform via a web browser so that I can use it easily.

---

### Use Cases

- **UC-1 [Show all Activities]**: Users can view all available activities.
- **UC-2 [Show Activity Details]**: Users can open a specific activity and see detailed information.
- **UC-3 [Search and Filter Activities]**: Users can search and filter activities by category, date, club, or location.
- **UC-4 [Favorite Club / Activity]**: Users can mark clubs and activities as favorites.
- **UC-5 [Join / Leave Activity]**: Users can register or unregister for an activity.
- **UC-6 [Manage Community Content]**: Users can create, edit, and delete community posts.
- **UC-7 [Post Announcement]**: Clubs can publish announcements related to their activities.

---

## Part 2: Design

### Design Overview
The design of FHNWConnect focuses on a clean, modern, and user-friendly interface suitable for a university environment.

A color scheme based on yellow, white, and light gray ensures visual consistency. Typography is simple and readable to improve accessibility.

The layout supports:
- **List view** for browsing activities efficiently  
- **Calendar view** for time-based navigation  

The user experience is optimized to allow students to discover activities quickly with minimal interaction.

---

### Wireframe

The wireframe defines the main structure of the application.

The interface is organized with a sidebar on the left, which serves as the main navigation:
- Home  
- Clubs  
- Sports  
- Community  

On the Home page:
- Calendar overview  
- Upcoming Activities  
- Favorite Clubs and Activities  

At the top:
- Search bar  
- Help, Login, and Sign Up  

---

### Prototype

The prototype demonstrates the visual design and interaction flow of the application.

#### 🏠 Home Dashboard
<img src="images/FHNW%20Connect_Home.png" width="700">

*Figure 1: Home dashboard with calendar and personalized content*

#### 🏫 Clubs Page
<img src="images/FHNW%20Connect_Clubs.png" width="700">

*Figure 2: Clubs overview with favorite functionality and activity sidebar*

#### 🏅 Sports Page
<img src="images/FHNW%20Connect_Sports.png" width="700">

*Figure 3: Weekly sports planner with join/leave functionality*

#### 💬 Community Page
<img src="images/FHNW%20Connect_Community.png" width="700">

*Figure 4: Community forum with posts, filters, and interactions*

---

### Domain Design

Main entities:
- User  
- Club  
- Activity  
- Community_Post  
- User_Activity  
- User_Favorite_Club  
- User_Favorite_Activity  

#### Entity Relationship Diagram (ERD)
<img src="images/Domain%20Model_FHNW%20Connect.png" width="800">

---

### Relationships

- A User can join multiple Activities via **User_Activity**  
- A User can favorite multiple Clubs and Activities  
- A User can create multiple Community Posts  
- A Club can organize multiple Activities  
- An Activity belongs to one Club  
- A Community Post is created by a User and may belong to a Club  

The **User_Activity** entity acts as a junction table between User and Activity and stores participation details such as status and timestamp.

---

### Business Logic

The business logic manages interactions between users, activities, and community features:

- Users can join or leave activities  
- Each user can only have one participation per activity  
- Favorites personalize the Home Dashboard  
- Users can create and manage community posts  
- Clubs can create activities and announcements  

---

### Example API

**Path:** `/api/activities/{activityId}/join`  
**Method:** POST  

**Request Body Example:**
```json
{
  "userId": 12,
  "status": "joined"
}
