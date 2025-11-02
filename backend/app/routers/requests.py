from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.ml_engine import predict_priority, predict_resolution_time

# Create router
router = APIRouter()


@router.post("/submit", response_model=schemas.RequestResponse)
def submit_service_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    """
    Submit a new service request
    Citizens use this endpoint to submit their requests
    AI automatically predicts priority and resolution time
    """
    
    # Step 1: Use AI to predict priority
    priority = predict_priority(request.request_type, request.location)
    
    # Step 2: Use AI to predict resolution time
    resolution_days = predict_resolution_time(priority, request.request_type)
    
    # Step 3: Create database entry
    db_request = models.ServiceRequest(
        citizen_name=request.citizen_name,
        email=request.email,
        phone=request.phone,
        request_type=request.request_type,
        location=request.location,
        description=request.description,
        priority=priority,
        predicted_resolution_days=resolution_days,
        status="Open"
    )
    
    # Step 4: Save to database
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    print(f"✅ New request submitted: ID={db_request.id}, Priority={priority}")
    
    return db_request


@router.get("/all", response_model=List[schemas.RequestResponse])
def get_all_requests(db: Session = Depends(get_db)):
    """
    Get all service requests
    Used by admin dashboard to see all citizen requests
    """
    
    requests = db.query(models.ServiceRequest).order_by(
        models.ServiceRequest.created_at.desc()
    ).all()
    
    print(f"📊 Retrieved {len(requests)} requests")
    
    return requests


@router.get("/{request_id}", response_model=schemas.RequestResponse)
def get_request_by_id(request_id: int, db: Session = Depends(get_db)):
    """
    Get a specific service request by ID
    Citizens can track their request status
    """
    
    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
    
    return request


@router.get("/priority/{priority_level}")
def get_requests_by_priority(priority_level: str, db: Session = Depends(get_db)):
    """
    Get all requests filtered by priority (High/Medium/Low)
    Helps admins focus on urgent requests
    """
    
    valid_priorities = ["High", "Medium", "Low"]
    
    if priority_level not in valid_priorities:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid priority. Must be one of: {valid_priorities}"
        )
    
    requests = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.priority == priority_level
    ).all()
    
    return {
        "priority": priority_level,
        "count": len(requests),
        "requests": requests
    }


@router.put("/{request_id}/status")
def update_request_status(
    request_id: int, 
    new_status: str, 
    db: Session = Depends(get_db)
):
    """
    Update the status of a request
    Admin can mark requests as: Open, In Progress, Resolved
    """
    
    valid_statuses = ["Open", "In Progress", "Resolved", "Closed"]
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
    
    old_status = request.status
    request.status = new_status
    
    db.commit()
    db.refresh(request)
    
    print(f"✅ Request {request_id} status updated: {old_status} → {new_status}")
    
    return {
        "message": f"Status updated successfully",
        "request_id": request_id,
        "old_status": old_status,
        "new_status": new_status
    }


@router.delete("/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    """
    Delete a service request (admin only)
    """
    
    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail=f"Request with ID {request_id} not found")
    
    db.delete(request)
    db.commit()
    
    print(f"🗑️ Request {request_id} deleted")
    
    return {"message": f"Request {request_id} deleted successfully"}
