"""
Lead scoring logic for lead enrichment system
"""

def calculate_lead_score(percent_renters, median_income, temperature):
    """
    Calculate lead score based on multiple factors
    
    Args:
        percent_renters (float): Percentage of renters in the area
        median_income (float): Median income in the area
        temperature (float): Current temperature in Fahrenheit
    
    Returns:
        int: Lead score from 0-100
    """
    
    # Normalize and weight each factor with more realistic ranges
    # Higher rental percentage = higher score (more potential customers)
    # More realistic: 0-40 points, with 50%+ renters needed for max score
    if percent_renters >= 60:
        rental_score = 40  # Excellent rental market
    elif percent_renters >= 50:
        rental_score = 35  # High rental market
    elif percent_renters >= 40:
        rental_score = 25  # Moderate rental market
    elif percent_renters >= 30:
        rental_score = 15  # Low rental market
    else:
        rental_score = 5   # Very low rental market
    
    # Higher income = higher score (more disposable income)
    # More realistic: 0-30 points, with $80k+ needed for max score
    if median_income >= 80000:
        income_score = 30  # High income area
    elif median_income >= 70000:
        income_score = 25  # Above average income
    elif median_income >= 60000:
        income_score = 20  # Average income
    elif median_income >= 50000:
        income_score = 15  # Below average income
    elif median_income >= 40000:
        income_score = 10  # Low income
    else:
        income_score = 5   # Very low income
    
    # Temperature factor (comfortable weather = higher engagement potential)
    # More realistic temperature scoring
    if 65 <= temperature <= 75:
        temp_score = 20  # Optimal temperature (narrower range)
    elif 60 <= temperature < 65 or 75 < temperature <= 80:
        temp_score = 15  # Good temperature
    elif 55 <= temperature < 60 or 80 < temperature <= 85:
        temp_score = 10  # Moderate temperature
    elif 50 <= temperature < 55 or 85 < temperature <= 90:
        temp_score = 5   # Poor temperature
    else:
        temp_score = 0   # Extreme temperature
    
    # Calculate total score
    total_score = rental_score + income_score + temp_score
    
    # Ensure score is within 0-100 range
    total_score = max(0, min(total_score, 100))
    
    return round(total_score)

def categorize_score(score):
    """
    Categorize lead score into High/Medium/Low
    
    Args:
        score (int): Lead score from 0-100
    
    Returns:
        str: Score category with emoji
    """
    if score >= 71:
        return "🟢 High"
    elif score >= 41:
        return "🟡 Medium"
    else:
        return "🔴 Low"

def get_score_breakdown(percent_renters, median_income, temperature):
    """
    Get detailed breakdown of score calculation
    
    Args:
        percent_renters (float): Percentage of renters in the area
        median_income (float): Median income in the area
        temperature (float): Current temperature in Fahrenheit
    
    Returns:
        dict: Score breakdown with individual components
    """
    
    # Calculate individual components using the new scoring logic
    if percent_renters >= 60:
        rental_score = 40
        rental_category = "Excellent"
    elif percent_renters >= 50:
        rental_score = 35
        rental_category = "High"
    elif percent_renters >= 40:
        rental_score = 25
        rental_category = "Moderate"
    elif percent_renters >= 30:
        rental_score = 15
        rental_category = "Low"
    else:
        rental_score = 5
        rental_category = "Very Low"
    
    if median_income >= 80000:
        income_score = 30
        income_category = "High"
    elif median_income >= 70000:
        income_score = 25
        income_category = "Above Average"
    elif median_income >= 60000:
        income_score = 20
        income_category = "Average"
    elif median_income >= 50000:
        income_score = 15
        income_category = "Below Average"
    elif median_income >= 40000:
        income_score = 10
        income_category = "Low"
    else:
        income_score = 5
        income_category = "Very Low"
    
    if 65 <= temperature <= 75:
        temp_score = 20
        temp_category = "Optimal"
    elif 60 <= temperature < 65 or 75 < temperature <= 80:
        temp_score = 15
        temp_category = "Good"
    elif 55 <= temperature < 60 or 80 < temperature <= 85:
        temp_score = 10
        temp_category = "Moderate"
    elif 50 <= temperature < 55 or 85 < temperature <= 90:
        temp_score = 5
        temp_category = "Poor"
    else:
        temp_score = 0
        temp_category = "Extreme"
    
    total_score = rental_score + income_score + temp_score
    total_score = max(0, min(total_score, 100))
    
    return {
        'total_score': round(total_score),
        'rental_score': rental_score,
        'income_score': income_score,
        'temp_score': temp_score,
        'temp_category': temp_category,
        'rental_category': rental_category,
        'income_category': income_category,
        'category': categorize_score(total_score),
        'breakdown': {
            'rental_percentage': f"{percent_renters:.1f}% renters ({rental_category}) → {rental_score} points",
            'median_income': f"${median_income:,.0f} income ({income_category}) → {income_score} points",
            'temperature': f"{temperature}°F ({temp_category}) → {temp_score} points"
        }
    }

def get_scoring_weights():
    """
    Get the scoring weights and explanation
    
    Returns:
        dict: Scoring weights and explanations
    """
    return {
        'weights': {
            'rental_percentage': 40,
            'median_income': 30,
            'temperature': 20,
            'bonus': 10
        },
        'explanations': {
            'rental_percentage': 'Higher rental percentage indicates more potential customers for property management services',
            'median_income': 'Higher income areas have more disposable income for premium services',
            'temperature': 'Comfortable weather conditions correlate with higher resident engagement',
            'bonus': 'Additional factors like walkability and local amenities'
        },
        'ranges': {
            'rental_percentage': '0-40 points (1.5x the percentage, capped at 40)',
            'median_income': '0-30 points (based on income above $30k threshold)',
            'temperature': '5-20 points (optimal 60-80°F gets 20 points)'
        }
    }
