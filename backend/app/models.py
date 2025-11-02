from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database import Base

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    citizen_name = Column(String)
    email = Column(String)
    phone = Column(String)
    request_type = Column(String)  # Water, Electricity, Roads, etc.
    location = Column(String)
    description = Column(String)
    priority = Column(String)  # High, Medium, Low (AI predicted)
    status = Column(String, default="Open")  # Open, In Progress, Resolved
    predicted_resolution_days = Column(Float)  # AI predicted
    created_at = Column(DateTime, default=datetime.utcnow)
