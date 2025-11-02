import random
from datetime import datetime, timedelta

def predict_priority(request_type, location):
    """
    AI-powered priority prediction based on request type and location
    
    Args:
        request_type (str): Type of service request
        location (str): Citizen's location
    
    Returns:
        str: Priority level (High/Medium/Low)
    """
    
    # Critical service types always get high priority
    high_priority_types = [
        'Water', 
        'Electricity', 
        'Medical', 
        'Emergency',
        'Fire',
        'Ambulance',
        'Gas Leak'
    ]
    
    # Important but not critical
    medium_priority_types = [
        'Roads',
        'Street Lights',
        'Garbage Collection',
        'Drainage',
        'Public Transport'
    ]
    
    # Rule-based AI logic
    if request_type in high_priority_types:
        return 'High'
    elif request_type in medium_priority_types:
        # Urban areas get higher priority for infrastructure
        if location.lower() in ['urban', 'city', 'metro', 'delhi', 'mumbai', 'bangalore', 'chennai']:
            return 'Medium'
        else:
            return 'Low'
    else:
        return 'Low'


def predict_resolution_time(priority, request_type):
    """
    Predict resolution time in days based on priority and request type
    
    Args:
        priority (str): Priority level (High/Medium/Low)
        request_type (str): Type of service request
    
    Returns:
        float: Estimated resolution time in days
    """
    
    # Base resolution time map based on priority
    base_resolution_map = {
        'High': (1, 3),      # 1-3 days
        'Medium': (3, 7),    # 3-7 days
        'Low': (7, 14)       # 7-14 days
    }
    
    # Request type complexity factor
    complex_requests = [
        'Roads', 
        'Construction', 
        'Building Permit',
        'Water Connection',
        'Electricity Connection'
    ]
    
    # Get base time range
    min_days, max_days = base_resolution_map.get(priority, (5, 10))
    
    # Add complexity factor
    if request_type in complex_requests:
        min_days += 2
        max_days += 3
    
    # Generate prediction with some randomness (simulating ML model)
    predicted_days = random.uniform(min_days, max_days)
    
    return round(predicted_days, 1)


def forecast_demand(historical_data=None):
    """
    Forecast future demand for services
    
    Args:
        historical_data: Past request data (optional)
    
    Returns:
        dict: Forecasted demand by service type
    """
    
    # Simulated forecast (in real scenario, use time series model)
    forecast = {
        'Water': {
            'current_demand': random.randint(20, 50),
            'predicted_next_week': random.randint(30, 60),
            'trend': 'increasing'
        },
        'Electricity': {
            'current_demand': random.randint(15, 40),
            'predicted_next_week': random.randint(20, 50),
            'trend': 'stable'
        },
        'Roads': {
            'current_demand': random.randint(10, 30),
            'predicted_next_week': random.randint(8, 25),
            'trend': 'decreasing'
        }
    }
    
    return forecast


def get_analytics_data(db_session=None):
    """
    Generate analytics for admin dashboard
    
    Args:
        db_session: Database session (optional)
    
    Returns:
        dict: Analytics data with predictions
    """
    
    # In real scenario, calculate from database
    # For now, returning simulated data
    
    analytics = {
        "total_requests": 145,
        "high_priority": 42,
        "medium_priority": 58,
        "low_priority": 45,
        "resolved": 98,
        "pending": 47,
        "in_progress": 15,
        "avg_resolution_time": 4.2,
        "efficiency_score": 87.5,  # Percentage of requests resolved on time
        
        # AI Predictions
        "predicted_tomorrow_requests": random.randint(15, 25),
        "bottleneck_areas": ["Delhi South", "Mumbai Central"],
        "recommended_focus": "Water and Electricity requests in urban areas"
    }
    
    return analytics


def identify_patterns(requests_list):
    """
    Identify patterns in service requests using AI
    
    Args:
        requests_list: List of service requests
    
    Returns:
        dict: Identified patterns and insights
    """
    
    patterns = {
        "peak_hours": ["9 AM - 11 AM", "2 PM - 4 PM"],
        "common_issues": ["Water Supply", "Electricity Outage"],
        "high_demand_locations": ["Sector 12", "Downtown", "Industrial Area"],
        "seasonal_trends": "Water requests increase in summer months",
        "recommendations": [
            "Deploy extra teams for water-related issues",
            "Increase response capacity during peak hours",
            "Focus on preventive maintenance in high-demand areas"
        ]
    }
    
    return patterns


def calculate_risk_score(request_type, location, wait_time_hours):
    """
    Calculate risk score for a request (how urgent it is becoming)
    
    Args:
        request_type: Type of request
        location: Location
        wait_time_hours: How long the request has been waiting
    
    Returns:
        int: Risk score (0-100)
    """
    
    base_risk = {
        'High': 70,
        'Medium': 40,
        'Low': 20
    }
    
    priority = predict_priority(request_type, location)
    risk = base_risk.get(priority, 30)
    
    # Increase risk based on wait time
    risk += min(wait_time_hours / 24 * 10, 30)  # Max 30 points for wait time
    
    return min(int(risk), 100)  # Cap at 100


# Additional utility functions

def get_sentiment_analysis(description):
    """
    Analyze sentiment of citizen's description (future enhancement)
    """
    # Placeholder for sentiment analysis
    # In production, use NLP model
    keywords_urgent = ['urgent', 'emergency', 'critical', 'immediate', 'help']
    
    description_lower = description.lower()
    
    for keyword in keywords_urgent:
        if keyword in description_lower:
            return 'urgent'
    
    return 'normal'


def recommend_resolution_strategy(request_type, priority):
    """
    Recommend best resolution strategy
    """
    strategies = {
        ('Water', 'High'): 'Deploy emergency water tanker immediately',
        ('Electricity', 'High'): 'Send emergency repair team',
        ('Roads', 'Medium'): 'Schedule repair crew within 48 hours',
        ('Garbage Collection', 'Low'): 'Add to next scheduled route'
    }
    
    return strategies.get((request_type, priority), 'Assign to appropriate department')
