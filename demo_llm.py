#!/usr/bin/env python3
"""
Demo script showing LLM vs Template outreach message generation
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.outreach import generate_outreach_message, generate_llm_outreach_message

def demo_outreach_comparison():
    """Demonstrate the difference between template and LLM-generated messages"""
    
    print("🤖 EliseAI Outreach Message Generation Demo")
    print("=" * 60)
    
    # Sample lead data
    lead_data = {
        'name': 'Jennifer Chen',
        'company': 'Bay Area Properties',
        'city': 'San Francisco',
        'state': 'CA',
        'weather_description': 'Clear Sky',
        'temperature': 63,
        'median_income': 95000,
        'percent_renters': 55,
        'population': 870000,
        'insights': 'high rental market, affluent area, temperate climate'
    }
    
    print("🌤️ Weather Conversion Examples:")
    print("-" * 40)
    weather_examples = [
        'Light Intensity Shower Rain',
        'Clear Sky',
        'Broken Clouds',
        'Heavy Intensity Shower Rain',
        'Thunderstorm with Heavy Rain'
    ]
    
    from utils.outreach import convert_weather_to_conversational
    for weather in weather_examples:
        conversational = convert_weather_to_conversational(weather)
        print(f"{weather:30} → {conversational}")
    print()
    
    print(f"📝 Lead: {lead_data['name']} from {lead_data['company']}")
    print(f"📍 Location: {lead_data['city']}, {lead_data['state']}")
    print(f"🌤️ Weather: {lead_data['weather_description']} ({lead_data['temperature']}°F)")
    print(f"💰 Demographics: ${lead_data['median_income']:,} income, {lead_data['percent_renters']}% renters")
    print(f"🏘️ Population: {lead_data['population']:,}")
    print(f"💡 Insights: {lead_data['insights']}")
    print()
    
    # Generate template-based message
    print("📝 TEMPLATE-BASED MESSAGE:")
    print("-" * 40)
    template_message = generate_outreach_message(
        lead_data['name'],
        lead_data['company'],
        lead_data['city'],
        lead_data['weather_description'],
        lead_data['insights']
    )
    print(template_message)
    print()
    
    # Generate LLM-based message (will fallback if no API key)
    print("🤖 AI-GENERATED MESSAGE:")
    print("-" * 40)
    try:
        llm_message = generate_llm_outreach_message(
            lead_data['name'],
            lead_data['company'],
            lead_data['city'],
            lead_data['state'],
            lead_data['weather_description'],
            lead_data['temperature'],
            lead_data['median_income'],
            lead_data['percent_renters'],
            lead_data['population'],
            lead_data['insights']
        )
        print(llm_message)
        print("\n✅ AI generation successful!")
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        print("📝 Using template fallback...")
        llm_message = generate_outreach_message(
            lead_data['name'],
            lead_data['company'],
            lead_data['city'],
            lead_data['weather_description'],
            lead_data['insights']
        )
        print(llm_message)
    
    print()
    print("🎯 KEY DIFFERENCES:")
    print("- Template: Uses predefined patterns and random selection")
    print("- AI: Analyzes all data points to create contextually relevant messages")
    print("- AI: More personalized and specific to local market conditions")
    print("- AI: Better connects weather, demographics, and EliseAI's value proposition")
    
    print()
    print("🔑 To enable AI generation:")
    print("1. Get OpenAI API key from https://platform.openai.com/api-keys")
    print("2. Add OPENAI_API_KEY=your_key_here to .env file")
    print("3. Restart the app")

def demo_multiple_leads():
    """Show how different leads get different AI-generated messages"""
    
    print("\n" + "=" * 60)
    print("🔄 Multiple Leads AI Generation Demo")
    print("=" * 60)
    
    leads = [
        {
            'name': 'Michael Rodriguez',
            'company': 'Seattle Living Properties',
            'city': 'Seattle',
            'state': 'WA',
            'weather': 'Broken Clouds',
            'temp': 56,
            'income': 75000,
            'renters': 50,
            'pop': 750000,
            'insights': 'moderate rental market, high-income area, cool climate'
        },
        {
            'name': 'Carlos Rodriguez',
            'company': 'Miami Properties Group',
            'city': 'Miami',
            'state': 'FL',
            'weather': 'Overcast Clouds',
            'temp': 75,
            'income': 55000,
            'renters': 45,
            'pop': 450000,
            'insights': 'moderate rental market, middle-income area, warm climate'
        }
    ]
    
    for i, lead in enumerate(leads, 1):
        print(f"\n📋 Lead {i}: {lead['name']} ({lead['company']})")
        print(f"   {lead['city']}, {lead['state']} - {lead['weather']} {lead['temp']}°F")
        print(f"   ${lead['income']:,} income, {lead['renters']}% renters")
        
        try:
            message = generate_llm_outreach_message(
                lead['name'], lead['company'], lead['city'], lead['state'],
                lead['weather'], lead['temp'], lead['income'], lead['renters'],
                lead['pop'], lead['insights']
            )
            print("   🤖 AI Message Preview:")
            # Show first 100 characters
            preview = message[:100] + "..." if len(message) > 100 else message
            print(f"   {preview}")
        except Exception as e:
            print(f"   ⚠️ AI failed: {e}")

def main():
    """Run the demo"""
    try:
        demo_outreach_comparison()
        demo_multiple_leads()
        
        print("\n🎉 Demo completed!")
        print("\nTo use the full app with AI generation:")
        print("   ./start_app.sh")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
