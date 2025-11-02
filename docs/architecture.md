# System Architecture

## Overview
GenAI Governance Platform uses a 3-tier architecture:

1. **Presentation Layer** - Frontend (HTML/CSS/JS)
2. **Application Layer** - Backend API (FastAPI)
3. **Data Layer** - Database (SQLite)

## Components

### Frontend
- Single-page application
- Responsive design
- Real-time API communication

### Backend
- RESTful API architecture
- 11 endpoints total
- AI/ML integration
- Automatic API documentation

### Database
- SQLite for portability
- SQLAlchemy ORM
- Single table: service_requests

### AI/ML Engine
- Priority prediction
- Resolution time estimation
- Demand forecasting
- Pattern recognition

## Data Flow

1. Citizen submits request → Frontend
2. Frontend sends JSON → Backend API
3. API validates data → Pydantic schemas
4. AI engine predicts priority/time
5. Data saved → SQLite database
6. Response returned → Frontend
7. Admin views analytics → Dashboard
