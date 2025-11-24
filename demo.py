#!/usr/bin/env python3
"""
Demo script for EliseAI Lead Enrichment App
Shows how the app works without running the full Streamlit interface
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.api_calls import get_mock_data
from utils.scoring import calculate_lead_score, categorize_score, get_score_breakdown
from utils.outreach import generate_outreach_message

def demo_lead_enrichment():
    """Demonstrate the lead enrichment process"""
    
    print("🏠 EliseAI Lead Enrichment Demo")
    print("=" * 50)
    
    # Sample lead data
    lead_data = {
        'name': 'Sarah Johnson',
        'email': 'sarah@metrorentals.com',
        'company': 'Metro Rentals LLC',
        'city': 'Austin',
        'state': 'TX',
        'country': 'USA'
    }
    
    print(f"📝 Processing lead: {lead_data['name']} from {lead_data['company']}")
    print(f"📍 Location: {lead_data['city']}, {lead_data['state']}, {lead_data['country']}")
    print()
    
    # Step 1: Enrich data (using mock data for demo)
    print("🔍 Step 1: Enriching lead data...")
    enriched_data = get_mock_data(lead_data['city'], lead_data['state'], lead_data['country'])
    
    print("   Weather Data:")
    print(f"   - Temperature: {enriched_data['temperature']}°F")
    print(f"   - Conditions: {enriched_data['weather_description']}")
    print(f"   - Humidity: {enriched_data['humidity']}%")
    print()
    
    print("   Demographic Data:")
    print(f"   - Population: {enriched_data['population']:,}")
    print(f"   - Median Income: ${enriched_data['median_income']:,}")
    print(f"   - % Renters: {enriched_data['percent_renters']:.1f}%")
    print()
    
    # Step 2: Calculate lead score
    print("📊 Step 2: Calculating lead score...")
    score = calculate_lead_score(
        enriched_data['percent_renters'],
        enriched_data['median_income'],
        enriched_data['temperature']
    )
    category = categorize_score(score)
    
    # Get detailed breakdown
    breakdown = get_score_breakdown(
        enriched_data['percent_renters'],
        enriched_data['median_income'],
        enriched_data['temperature']
    )
    
    print(f"   Total Score: {score}/100 ({category})")
    print("   Score Breakdown:")
    print(f"   - Rental Market: {breakdown['rental_score']:.1f}/40 points")
    print(f"   - Income Level: {breakdown['income_score']:.1f}/30 points")
    print(f"   - Temperature: {breakdown['temp_score']}/20 points")
    print()
    
    # Step 3: Generate insights
    print("💡 Step 3: Generating insights...")
    insights = []
    
    if enriched_data['percent_renters'] > 50:
        insights.append("high rental market")
    elif enriched_data['percent_renters'] > 30:
        insights.append("moderate rental market")
    else:
        insights.append("low rental market")
    
    if enriched_data['median_income'] > 75000:
        insights.append("affluent area")
    elif enriched_data['median_income'] > 50000:
        insights.append("middle-income area")
    else:
        insights.append("budget-conscious area")
    
    if enriched_data['temperature'] > 80:
        insights.append("warm climate")
    elif enriched_data['temperature'] < 40:
        insights.append("cool climate")
    else:
        insights.append("temperate climate")
    
    insights_text = ", ".join(insights)
    print(f"   Insights: {insights_text}")
    print()
    
    # Step 4: Generate outreach message
    print("💬 Step 4: Generating personalized outreach message...")
    outreach_message = generate_outreach_message(
        lead_data['name'],
        lead_data['company'],
        lead_data['city'],
        enriched_data['weather_description'],
        insights_text
    )
    
    print("   Generated Message:")
    print("   " + "-" * 40)
    for line in outreach_message.split('\n'):
        print(f"   {line}")
    print("   " + "-" * 40)
    print()
    
    # Summary
    print("✅ Lead enrichment complete!")
    print(f"   Lead: {lead_data['name']} ({lead_data['company']})")
    print(f"   Score: {score}/100 ({category})")
    print(f"   Priority: {'High' if score >= 71 else 'Medium' if score >= 41 else 'Low'}")
    print()
    
    return {
        'lead_data': lead_data,
        'enriched_data': enriched_data,
        'score': score,
        'category': category,
        'insights': insights_text,
        'outreach_message': outreach_message
    }

def demo_multiple_leads():
    """Demonstrate processing multiple leads"""
    
    print("\n🔄 Processing Multiple Leads Demo")
    print("=" * 50)
    
    leads = [
        {'name': 'John Smith', 'company': 'ABC Properties', 'city': 'San Francisco', 'state': 'CA'},
        {'name': 'Maria Garcia', 'company': 'Sunset Rentals', 'city': 'Miami', 'state': 'FL'},
        {'name': 'David Chen', 'company': 'Urban Living', 'city': 'Seattle', 'state': 'WA'},
    ]
    
    results = []
    
    for i, lead in enumerate(leads, 1):
        print(f"\n📋 Lead {i}: {lead['name']} ({lead['company']})")
        
        # Get mock data
        enriched_data = get_mock_data(lead['city'], lead['state'], 'USA')
        
        # Calculate score
        score = calculate_lead_score(
            enriched_data['percent_renters'],
            enriched_data['median_income'],
            enriched_data['temperature']
        )
        category = categorize_score(score)
        
        results.append({
            'name': lead['name'],
            'company': lead['company'],
            'city': lead['city'],
            'score': score,
            'category': category
        })
        
        print(f"   Score: {score}/100 ({category})")
    
    # Summary table
    print(f"\n📊 Summary of All Leads:")
    print("   " + "-" * 60)
    print(f"   {'Name':<15} {'Company':<15} {'City':<12} {'Score':<8} {'Category'}")
    print("   " + "-" * 60)
    
    for result in results:
        print(f"   {result['name']:<15} {result['company']:<15} {result['city']:<12} {result['score']:<8} {result['category']}")
    
    print("   " + "-" * 60)
    
    # Find highest scoring lead
    best_lead = max(results, key=lambda x: x['score'])
    print(f"\n🏆 Highest scoring lead: {best_lead['name']} ({best_lead['company']}) with {best_lead['score']}/100")

def main():
    """Run the demo"""
    try:
        # Single lead demo
        demo_lead_enrichment()
        
        # Multiple leads demo
        demo_multiple_leads()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the full Streamlit app:")
        print("   ./start_app.sh")
        print("   or")
        print("   streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
