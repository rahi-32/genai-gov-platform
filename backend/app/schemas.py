from pydantic import BaseModel
from datetime import datetime

class RequestCreate(BaseModel):
    citizen_name: str
    email: str
    phone: str
    request_type: str
    location: str
    description: str

class RequestResponse(BaseModel):
    id: int
    citizen_name: str
    request_type: str
    location: str
    priority: str
    status: str
    predicted_resolution_days: float
    created_at: datetime
    
    class Config:
        from_attributes = True
