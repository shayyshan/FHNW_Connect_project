# FHNW Connect

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Budibase](https://img.shields.io/badge/Budibase-Low_Code-yellow)
![Render](https://img.shields.io/badge/Render-Deployed-purple)

FHNW Connect is a campus engagement platform developed as part of the Internet Technology Project at FHNW Brugg.

The platform centralizes clubs, sports activities, and community interactions into a single application, helping students discover events, connect with communities, and stay informed about campus life.

---

# Live Demo

### Frontend (Budibase)

https://inttech.budibase.app/app/brugg_2_fhnw_connect/brugg2fhnwconnect

### Backend API (Render)

https://fhnw-connect-project.onrender.com

### GitHub Repository

https://github.com/shayyshan/FHNW_Connect_project

---

# Project Overview

FHNW Connect provides a centralized platform where students can:

- Discover upcoming campus activities
- Explore student clubs
- Browse sports events
- Mark clubs as favorites
- View personalized content
- Participate in community discussions
- Create community posts
- Access activity information through calendar views

The goal of the project is to improve student engagement and create a single point of access for campus activities and information.

---

# User Stories

## Students

- As a Student, I want to view upcoming campus activities so that I know what is happening at FHNW.
- As a Student, I want to browse clubs so that I can find communities that match my interests.
- As a Student, I want to mark clubs as favorites so that I can quickly access them later.
- As a Student, I want to browse sports activities through a calendar interface.
- As a Student, I want to view detailed information about sports activities.
- As a Student, I want to browse community discussions.
- As a Student, I want to create community posts.
- As a User, I want an intuitive interface so that I can easily navigate the platform.

---

# Use Cases

| ID | Use Case |
|------|------|
| UC-1 | View Home Dashboard |
| UC-2 | Browse Clubs |
| UC-3 | Favorite Club |
| UC-4 | View Sports Calendar |
| UC-5 | View Sports Activity Details |
| UC-6 | Browse Community Posts |
| UC-7 | Create Community Post |
| UC-8 | View Personalized Content |

---

# Design Overview

The application follows a clean and modern design inspired by FHNW branding.

## Design Principles

- Simple navigation
- Consistent visual appearance
- Calendar-based activity planning
- Card-based content presentation
- Responsive layout
- User-friendly interaction patterns

## Color Palette

- FHNW Yellow
- White
- Light Gray
- Black

---

# Application Structure

The application consists of four major modules.

## Home

The Home Dashboard provides:

- Monthly calendar overview
- Upcoming activities
- Favorite clubs
- Favorite sports
- Personalized content

## Clubs

The Clubs section allows users to:

- Browse clubs
- View club information
- Mark clubs as favorites
- View announcements
- Discover upcoming activities

## Sports

The Sports module provides:

- Weekly calendar view
- Monthly calendar view
- Daily calendar view
- Agenda view
- Activity details

## Community

The Community module provides:

- Community forum
- Community post creation
- Categorized discussions
- Student interaction platform

---

# Screenshots

## Home Dashboard

<img src="images/FHNW Connect_Home.png" width="1000">

### Features

- Calendar overview
- Upcoming activities
- Favorite clubs
- Favorite sports

*Figure 1: Home Dashboard*

---

## Clubs Module

<img src="images/FHNW Connect_Clubs.png" width="1000">

### Features

- Club overview cards
- Favorite club functionality
- Upcoming activities section
- Announcements section

*Figure 2: Clubs Page*

---

## Sports Module – Calendar View

<img src="images/FHNW Connect_Sports_1.png" width="1000">

### Features

- Weekly calendar
- Activity scheduling
- Calendar navigation
- Multiple calendar views

*Figure 3: Sports Calendar*

---

## Sports Module – Activity Details

<img src="images/FHNW Connect_Sports_2.png" width="700">

### Features

- Activity description
- Location information
- Date and time display
- Activity image

*Figure 4: Sports Activity Details Modal*

---

## Community Module

<img src="images/FHNW Connect_Community_1.png" width="1000">

### Features

- Community discussions
- Categorized posts
- Forum overview

*Figure 5: Community Forum*

---

## Community Post Creation

<img src="images/FHNW Connect_Community_2.png" width="700">

### Features

- Create post dialog
- Title field
- Description field
- Category field
- Keyword field

*Figure 6: Community Post Creation Modal*

---

# Domain-Driven Design

The project follows Domain-Driven Design (DDD) principles and separates the business logic into bounded contexts.

## Domain Model

<img src="images/Domain Model_FHNW Connect.png" width="1100">

*Figure 7: FHNW Connect Domain Model*

---

# Bounded Contexts

## Activity Participation (Core Domain)

Responsible for:

- Activities
- Sports activities
- User participation
- Favorite activities

### Entities

- Activity
- Sport
- User_Activity
- User_Favorite_Activity

---

## Club Management (Supporting Domain)

Responsible for:

- Club administration
- Club information
- Favorite clubs

### Entities

- Club
- User_Favorite_Club

---

## Community Content (Supporting Domain)

Responsible for:

- Community discussions
- Community posts

### Entities

- Community_Post

---

## User Management (Generic Domain)

Responsible for:

- User accounts
- User information

### Entities

- User

---

# Relationships

- A Club can organize multiple Activities.
- Activities belong to a Club.
- Users can register for Activities through User_Activity.
- Users can mark Clubs as favorites.
- Users can mark Activities and Sports as favorites.
- Users can create Community Posts.
- Community Posts may be associated with a Club.
- Sports activities are managed independently within the Activity Participation domain.

---

# Business Logic

## Club Management

- Browse clubs
- View club information
- Mark clubs as favorites
- Display favorite clubs on the dashboard

## Sports Activities

- Display activities in calendar views
- View activity details
- Manage schedules and event information

## Community Features

- Browse community posts
- Create new community posts
- Organize posts using categories

## Personalization

- Favorite clubs displayed on dashboard
- Favorite sports displayed on dashboard
- Upcoming activities highlighted on the home page

---

# System Architecture

```text
Budibase Frontend
        │
        ▼
FastAPI Backend (Render)
        │
        ▼
SQLAlchemy ORM
        │
        ▼
PostgreSQL Database (Render)
```

The frontend communicates with the backend through REST APIs. The FastAPI backend processes requests, handles business logic, and persists data in PostgreSQL using SQLAlchemy.

---

# Technologies Used

## Frontend

- Budibase
- JavaScript
- Responsive Web Design

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL

## Database Migration

- Alembic

## Deployment

- Render
- Budibase Cloud

## Version Control

- GitHub

## Design & Modeling

- Domain-Driven Design (DDD)
- Entity Relationship Modeling (ERD)
- Bounded Context Design

---

# Deployment

## Frontend

Hosted on Budibase Cloud:

https://inttech.budibase.app/app/brugg_2_fhnw_connect/brugg2fhnwconnect

## Backend

Hosted on Render:

https://fhnw-connect-project.onrender.com

## Database

PostgreSQL database hosted on Render.

Database credentials are managed through environment variables and are not included in the repository.

---

# Local Development Setup

## Prerequisites

- Python 3.11+
- PostgreSQL
- Git

## Clone Repository

```bash
git clone https://github.com/shayyshan/FHNW_Connect_project.git
cd FHNW_Connect_project
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

FastAPI automatically generates API documentation:

```text
http://localhost:8000/docs
```

---

# Authors

### Shannon Polak

FHNW Brugg – Internet Technology Project

GitHub:
https://github.com/shayyshan

---

# Final Result

FHNW Connect successfully integrates:

✅ Home Dashboard

✅ Club Management

✅ Favorite Clubs

✅ Sports Calendar

✅ Sports Activity Details

✅ Community Forum

✅ Community Post Creation

✅ Personalized Content

✅ PostgreSQL Integration

✅ FastAPI Backend

✅ Budibase Frontend

✅ Cloud Deployment

✅ Domain-Driven Design Architecture

The project demonstrates the complete software development lifecycle, from requirements analysis and domain modeling to the implementation and deployment of a functional campus engagement platform for FHNW students.