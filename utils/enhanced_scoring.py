"""
Enhanced Lead Scoring with CRM and Clay Data
Extends base scoring with additional data sources
"""

from typing import Dict, Optional
from .scoring import calculate_lead_score, categorize_score

def calculate_enhanced_lead_score(
    percent_renters: float,
    median_income: float,
    temperature: float,
    crm_engagement_score: Optional[float] = None,
    clay_company_data: Optional[Dict] = None,
    historical_data: Optional[Dict] = None
) -> int:
    """
    Calculate enhanced lead score with additional data sources
    
    Args:
        percent_renters: Percentage of renters in the area
        median_income: Median household income
        temperature: Current temperature
        crm_engagement_score: Engagement score from CRM (0-100)
        clay_company_data: Company data from Clay enrichment
        historical_data: Historical interaction data
    
    Returns:
        int: Enhanced lead score from 0-100
    """
    # Base score (existing algorithm)
    base_score = calculate_lead_score(percent_renters, median_income, temperature)
    
    # CRM engagement bonus (0-10 points)
    crm_bonus = 0
    if crm_engagement_score is not None:
        # Normalize engagement score to 0-10 points
        crm_bonus = min(10, crm_engagement_score / 10)
    
    # Clay company data bonus (0-10 points)
    clay_bonus = 0
    if clay_company_data:
        # Company size bonus (0-3 points)
        employee_count = clay_company_data.get('employee_count', 0)
        if employee_count > 200:
            clay_bonus += 3
        elif employee_count > 50:
            clay_bonus += 2
        elif employee_count > 10:
            clay_bonus += 1
        
        # Revenue bonus (0-3 points)
        revenue = clay_company_data.get('revenue', 0)
        if revenue > 10000000:  # $10M+
            clay_bonus += 3
        elif revenue > 1000000:  # $1M+
            clay_bonus += 2
        elif revenue > 100000:  # $100K+
            clay_bonus += 1
        
        # Industry fit bonus (0-2 points)
        # Property management related industries
        property_related_industries = [
            'real estate', 'property management', 'housing', 
            'construction', 'facilities management'
        ]
        industry = clay_company_data.get('industry', '').lower()
        if any(prop_ind in industry for prop_ind in property_related_industries):
            clay_bonus += 2
        
        # Funding stage bonus (0-2 points)
        funding = clay_company_data.get('total_funding', 0)
        if funding > 10000000:  # $10M+
            clay_bonus += 2
        elif funding > 1000000:  # $1M+
            clay_bonus += 1
    
    # Historical data bonus (0-10 points)
    history_bonus = 0
    if historical_data:
        # Previous interaction bonus (0-3 points)
        if historical_data.get('has_previous_interaction', False):
            history_bonus += 3
        
        # Conversion probability bonus (0-3 points)
        conversion_prob = historical_data.get('conversion_probability', 0)
        if conversion_prob > 0.7:
            history_bonus += 3
        elif conversion_prob > 0.5:
            history_bonus += 2
        elif conversion_prob > 0.3:
            history_bonus += 1
        
        # Deal history bonus (0-2 points)
        if historical_data.get('has_deal_history', False):
            history_bonus += 2
        
        # Time in CRM bonus (0-2 points)
        # Recent leads get bonus (within last 30 days)
        days_in_crm = historical_data.get('days_in_crm', 999)
        if days_in_crm < 30:
            history_bonus += 2
        elif days_in_crm < 90:
            history_bonus += 1
    
    # Calculate total score
    total_score = base_score + crm_bonus + clay_bonus + history_bonus
    
    # Ensure score is within 0-100 range
    total_score = max(0, min(100, total_score))
    
    return round(total_score)

def get_enhanced_score_breakdown(
    percent_renters: float,
    median_income: float,
    temperature: float,
    crm_engagement_score: Optional[float] = None,
    clay_company_data: Optional[Dict] = None,
    historical_data: Optional[Dict] = None
) -> Dict:
    """
    Get detailed breakdown of enhanced score calculation
    
    Args:
        percent_renters: Percentage of renters in the area
        median_income: Median household income
        temperature: Current temperature
        crm_engagement_score: Engagement score from CRM
        clay_company_data: Company data from Clay
        historical_data: Historical interaction data
    
    Returns:
        dict: Detailed score breakdown
    """
    from .scoring import get_score_breakdown
    
    # Get base breakdown
    base_breakdown = get_score_breakdown(percent_renters, median_income, temperature)
    
    # Calculate bonuses
    crm_bonus = 0
    if crm_engagement_score is not None:
        crm_bonus = min(10, crm_engagement_score / 10)
    
    clay_bonus = 0
    clay_details = []
    if clay_company_data:
        employee_count = clay_company_data.get('employee_count', 0)
        if employee_count > 200:
            clay_bonus += 3
            clay_details.append(f"Large company ({employee_count} employees) → +3 points")
        elif employee_count > 50:
            clay_bonus += 2
            clay_details.append(f"Medium company ({employee_count} employees) → +2 points")
        elif employee_count > 10:
            clay_bonus += 1
            clay_details.append(f"Small company ({employee_count} employees) → +1 point")
        
        revenue = clay_company_data.get('revenue', 0)
        if revenue > 10000000:
            clay_bonus += 3
            clay_details.append(f"High revenue (${revenue/1000000:.1f}M+) → +3 points")
        elif revenue > 1000000:
            clay_bonus += 2
            clay_details.append(f"Medium revenue (${revenue/1000000:.1f}M+) → +2 points")
        elif revenue > 100000:
            clay_bonus += 1
            clay_details.append(f"Low revenue (${revenue/1000:.0f}K+) → +1 point")
    
    history_bonus = 0
    history_details = []
    if historical_data:
        if historical_data.get('has_previous_interaction', False):
            history_bonus += 3
            history_details.append("Previous interaction → +3 points")
        
        conversion_prob = historical_data.get('conversion_probability', 0)
        if conversion_prob > 0.7:
            history_bonus += 3
            history_details.append(f"High conversion probability ({conversion_prob:.0%}) → +3 points")
        elif conversion_prob > 0.5:
            history_bonus += 2
            history_details.append(f"Medium conversion probability ({conversion_prob:.0%}) → +2 points")
        elif conversion_prob > 0.3:
            history_bonus += 1
            history_details.append(f"Low conversion probability ({conversion_prob:.0%}) → +1 point")
    
    total_score = base_breakdown['total_score'] + crm_bonus + clay_bonus + history_bonus
    total_score = max(0, min(100, total_score))
    
    return {
        'total_score': round(total_score),
        'base_score': base_breakdown['total_score'],
        'crm_bonus': round(crm_bonus, 1),
        'clay_bonus': round(clay_bonus, 1),
        'history_bonus': round(history_bonus, 1),
        'category': categorize_score(total_score),
        'base_breakdown': base_breakdown,
        'enhancement_details': {
            'crm_engagement': f"CRM engagement score: {crm_engagement_score or 'N/A'} → +{crm_bonus:.1f} points" if crm_engagement_score else None,
            'clay_insights': clay_details if clay_details else None,
            'historical_insights': history_details if history_details else None
        }
    }

