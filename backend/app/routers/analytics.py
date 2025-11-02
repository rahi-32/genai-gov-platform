from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models
from app.ml_engine import get_analytics_data, forecast_demand, identify_patterns

# Create router
router = APIRouter()


@router.get("/dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db)):
    """
    Main dashboard analytics
    Shows real-time statistics and AI predictions
    """
    
    # Get counts from database
    total = db.query(models.ServiceRequest).count()
    
    high_priority = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.priority == "High"
    ).count()
    
    medium_priority = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.priority == "Medium"
    ).count()
    
    low_priority = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.priority == "Low"
    ).count()
    
    open_requests = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.status == "Open"
    ).count()
    
    in_progress = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.status == "In Progress"
    ).count()
    
    resolved = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.status == "Resolved"
    ).count()
    
    # Calculate average resolution time
    avg_resolution = db.query(
        func.avg(models.ServiceRequest.predicted_resolution_days)
    ).scalar() or 0
    
    # Get recent requests
    recent_requests = db.query(models.ServiceRequest).order_by(
        models.ServiceRequest.created_at.desc()
    ).limit(10).all()
    
    return {
        "total_requests": total,
        "priority_breakdown": {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        },
        "status_breakdown": {
            "open": open_requests,
            "in_progress": in_progress,
            "resolved": resolved
        },
        "avg_resolution_time": round(avg_resolution, 1),
        "recent_requests": recent_requests,
        "ai_predictions": get_analytics_data()
    }


@router.get("/forecast")
def get_demand_forecast():
    """
    AI-powered demand forecasting
    Predicts future service demand
    """
    
    forecast = forecast_demand()
    
    return {
        "message": "Demand forecast for next 7 days",
        "forecast": forecast
    }


@router.get("/patterns")
def get_request_patterns(db: Session = Depends(get_db)):
    """
    Identify patterns in service requests
    Helps in proactive planning
    """
    
    # Get all requests for pattern analysis
    all_requests = db.query(models.ServiceRequest).all()
    
    patterns = identify_patterns(all_requests)
    
    return {
        "total_requests_analyzed": len(all_requests),
        "patterns": patterns
    }


@router.get("/statistics")
def get_detailed_statistics(db: Session = Depends(get_db)):
    """
    Detailed statistics for reporting
    """
    
    # Request type distribution
    request_types = db.query(
        models.ServiceRequest.request_type,
        func.count(models.ServiceRequest.id)
    ).group_by(models.ServiceRequest.request_type).all()
    
    # Location-wise distribution
    locations = db.query(
        models.ServiceRequest.location,
        func.count(models.ServiceRequest.id)
    ).group_by(models.ServiceRequest.location).all()
    
    # Priority distribution over time
    priority_stats = db.query(
        models.ServiceRequest.priority,
        func.count(models.ServiceRequest.id)
    ).group_by(models.ServiceRequest.priority).all()
    
    return {
        "request_type_distribution": [
            {"type": rt, "count": count} for rt, count in request_types
        ],
        "location_distribution": [
            {"location": loc, "count": count} for loc, count in locations
        ],
        "priority_distribution": [
            {"priority": pri, "count": count} for pri, count in priority_stats
        ]
    }


@router.get("/efficiency")
def get_efficiency_metrics(db: Session = Depends(get_db)):
    """
    Calculate system efficiency metrics
    """
    
    total = db.query(models.ServiceRequest).count()
    resolved = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.status == "Resolved"
    ).count()
    
    efficiency = (resolved / total * 100) if total > 0 else 0
    
    return {
        "total_requests": total,
        "resolved_requests": resolved,
        "efficiency_percentage": round(efficiency, 2),
        "pending_requests": total - resolved
    }
