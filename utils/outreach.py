"""
Outreach message generation for lead enrichment system
"""

import random
import os
from openai import OpenAI

def convert_weather_to_conversational(weather_description):
    """
    Convert technical weather descriptions to conversational language
    
    Args:
        weather_description (str): Technical weather description from API
    
    Returns:
        str: Conversational weather description
    """
    weather_mapping = {
        # Clear skies
        'clear sky': 'beautiful sunny weather',
        'clear': 'beautiful sunny weather',
        'sunny': 'sunny weather',
        
        # Clouds
        'few clouds': 'mostly sunny weather',
        'scattered clouds': 'partly cloudy weather',
        'broken clouds': 'partly cloudy weather',
        'overcast clouds': 'cloudy weather',
        'overcast': 'cloudy weather',
        'cloudy': 'cloudy weather',
        
        # Rain
        'light rain': 'light rain',
        'moderate rain': 'rainy weather',
        'heavy rain': 'heavy rain',
        'very heavy rain': 'heavy rain',
        'extreme rain': 'heavy rain',
        'freezing rain': 'freezing rain',
        'light intensity shower rain': 'light rain',
        'shower rain': 'rainy weather',
        'heavy intensity shower rain': 'heavy rain',
        'ragged shower rain': 'rainy weather',
        'light intensity drizzle': 'light drizzle',
        'drizzle': 'light drizzle',
        'heavy intensity drizzle': 'heavy drizzle',
        'light intensity drizzle rain': 'light rain',
        'drizzle rain': 'light rain',
        'heavy intensity drizzle rain': 'rainy weather',
        'shower rain and drizzle': 'rainy weather',
        'heavy shower rain and drizzle': 'heavy rain',
        'shower drizzle': 'light rain',
        
        # Snow
        'light snow': 'light snow',
        'snow': 'snowy weather',
        'heavy snow': 'heavy snow',
        'sleet': 'sleety weather',
        'light shower sleet': 'light sleet',
        'shower sleet': 'sleety weather',
        'light rain and snow': 'light wintry mix',
        'rain and snow': 'wintry mix',
        'light shower snow': 'light snow',
        'shower snow': 'snowy weather',
        'heavy shower snow': 'heavy snow',
        
        # Storms
        'thunderstorm': 'stormy weather',
        'thunderstorm with light rain': 'light storm',
        'thunderstorm with rain': 'stormy weather',
        'thunderstorm with heavy rain': 'heavy storm',
        'light thunderstorm': 'light storm',
        'heavy thunderstorm': 'heavy storm',
        'ragged thunderstorm': 'stormy weather',
        'thunderstorm with light drizzle': 'light storm',
        'thunderstorm with drizzle': 'stormy weather',
        'thunderstorm with heavy drizzle': 'heavy storm',
        
        # Fog and mist
        'mist': 'misty weather',
        'fog': 'foggy weather',
        'foggy': 'foggy weather',
        'haze': 'hazy weather',
        'smoke': 'smoky weather',
        'dust': 'dusty weather',
        'sand': 'sandy weather',
        'ash': 'ashy weather',
        'squalls': 'windy weather',
        'tornado': 'stormy weather',
        'tropical storm': 'stormy weather',
        'hurricane': 'stormy weather',
        'cold': 'cold weather',
        'hot': 'hot weather',
        'windy': 'windy weather',
        'hail': 'hail',
    }
    
    # Convert to lowercase for matching
    weather_lower = weather_description.lower().strip()
    
    # Try exact match first
    if weather_lower in weather_mapping:
        return weather_mapping[weather_lower]
    
    # Try partial matches
    for technical_term, conversational_term in weather_mapping.items():
        if technical_term in weather_lower:
            return conversational_term
    
    # If no match found, try to make it more conversational
    if 'rain' in weather_lower:
        return 'rainy weather'
    elif 'snow' in weather_lower:
        return 'snowy weather'
    elif 'cloud' in weather_lower:
        return 'cloudy weather'
    elif 'clear' in weather_lower or 'sun' in weather_lower:
        return 'sunny weather'
    elif 'storm' in weather_lower or 'thunder' in weather_lower:
        return 'stormy weather'
    elif 'fog' in weather_lower or 'mist' in weather_lower:
        return 'foggy weather'
    else:
        # Default fallback
        return 'pleasant weather'

def generate_llm_outreach_message(name, company, city, state, weather_description, temperature, 
                                 median_income, percent_renters, population, insights):
    """
    Generate personalized outreach message using OpenAI LLM
    
    Args:
        name (str): Lead's name
        company (str): Company name
        city (str): City name
        state (str): State name
        weather_description (str): Weather description
        temperature (float): Current temperature
        median_income (float): Median income in the area
        percent_renters (float): Percentage of renters
        population (int): Population of the area
        insights (str): Generated insights about the area
    
    Returns:
        str: LLM-generated personalized outreach message
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Create context-rich prompt
        prompt = f"""
You are a sales representative for a property management technology company that helps automate resident communications and streamline operations.

Generate a personalized, professional outreach email for a property management lead with the following details:

LEAD INFORMATION:
- Name: {name}
- Company: {company}
- Location: {city}, {state}
- Current Weather: {weather_description} ({temperature}°F)
- Area Demographics: {population:,} population, ${median_income:,} median income, {percent_renters:.1f}% renters
- Market Insights: {insights}

VALUE PROPOSITIONS:
- Automate resident communications (maintenance requests, announcements, rent reminders)
- Reduce administrative overhead and save time
- Improve resident satisfaction and retention
- Streamline property management operations
- Provide data-driven insights for better decision making
- Scale communication across multiple properties

REQUIREMENTS:
1. Start with a personalized greeting using their name
2. Reference the current weather in their city naturally
3. Connect their local market conditions to the value proposition
4. Mention specific benefits relevant to their demographic profile
5. Include a clear call-to-action for a conversation
6. Keep it professional but conversational (2-3 paragraphs)
7. End with a professional signature placeholder
8. Make it feel personal and relevant to their specific situation

TONE: Professional, helpful, consultative, not pushy
LENGTH: 150-250 words
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert sales representative specializing in property management technology. Write compelling, personalized outreach emails that connect local market conditions to the value proposition."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"LLM generation failed: {e}")
        # Fall back to template-based generation
        return generate_outreach_message(name, company, city, weather_description, insights)

def generate_outreach_message(name, company, city, weather_description, insights):
    """
    Generate personalized outreach message based on enriched data (fallback method)
    
    Args:
        name (str): Lead's name
        company (str): Company name
        city (str): City name
        weather_description (str): Weather description
        insights (str): Generated insights about the area
    
    Returns:
        str: Personalized outreach message
    """
    
    # Convert weather to conversational first
    conversational_weather = convert_weather_to_conversational(weather_description)
    
    # Greeting variations
    greetings = [
        f"Hi {name},",
        f"Hello {name},",
        f"Hi there {name},",
    ]
    
    # Weather-related openings
    weather_openings = [
        f"Hope you're enjoying the {conversational_weather} in {city}!",
        f"How's the {conversational_weather} treating you in {city}?",
        f"Hope the {conversational_weather} in {city} is treating you well!",
        f"Enjoying the {conversational_weather} in {city}?",
    ]
    
    # Insight-based value propositions
    insight_templates = {
        'high rental market': [
            f"I noticed {company} manages properties in an area with a high rental market — that's a great opportunity for resident engagement and retention.",
            f"With {company} operating in a high rental market area, there's tremendous potential for improving resident satisfaction and reducing turnover.",
            f"Managing properties in a high rental market like yours presents unique opportunities for streamlining communications and operations.",
        ],
        'moderate rental market': [
            f"I noticed {company} manages properties in an area with a moderate rental market — there's solid potential for enhancing resident engagement.",
            f"With {company} in a moderate rental market, there are good opportunities to differentiate through superior resident communication.",
            f"Operating in a moderate rental market gives {company} the chance to stand out with exceptional resident services.",
        ],
        'low rental market': [
            f"I noticed {company} manages properties in an area with a lower rental market — perfect for focusing on quality resident experiences.",
            f"With {company} in a lower rental market, there's an opportunity to provide premium resident communication services.",
            f"Managing properties in a lower rental market allows {company} to focus on delivering exceptional resident satisfaction.",
        ],
        'affluent area': [
            f"I noticed {company} manages properties in an affluent area — residents likely expect premium communication and service levels.",
            f"With {company} serving an affluent community, there's an opportunity to provide sophisticated resident engagement solutions.",
            f"Operating in an affluent area means {company} can leverage technology to meet high resident expectations.",
        ],
        'middle-income area': [
            f"I noticed {company} manages properties in a middle-income area — there's great potential for cost-effective resident engagement solutions.",
            f"With {company} in a middle-income market, there are opportunities to provide value-driven resident communication services.",
            f"Serving a middle-income community allows {company} to balance quality service with operational efficiency.",
        ],
        'budget-conscious area': [
            f"I noticed {company} manages properties in a budget-conscious area — there's an opportunity to provide efficient, cost-effective resident services.",
            f"With {company} in a budget-conscious market, there's potential to deliver high-value resident communication solutions.",
            f"Operating in a budget-conscious area means {company} can focus on practical, efficient resident engagement.",
        ]
    }
    
    # Value proposition variations
    value_props = [
        "We help property managers automate communications and save time while improving resident satisfaction.",
        "We specialize in helping property managers streamline resident communications and reduce administrative overhead.",
        "We help property management companies enhance resident engagement through intelligent communication automation.",
        "We provide property managers with tools to automate routine communications and focus on what matters most.",
    ]
    
    # Call to action variations
    ctas = [
        "Would you be open to a quick chat this week to discuss how we might help?",
        "I'd love to schedule a brief call to explore how we could benefit your operations.",
        "Would you be interested in a short conversation about how we could help streamline your resident communications?",
        "Could we schedule a quick call to discuss how we might fit into your property management strategy?",
    ]
    
    # Closing variations
    closings = [
        "Best regards,\n[Your Name]\n[Company Name]",
        "Looking forward to connecting,\n[Your Name]\n[Company Name]",
        "Thanks for your time,\n[Your Name]\n[Company Name]",
        "Best,\n[Your Name]\n[Company Name]",
    ]
    
    # Select random elements
    greeting = random.choice(greetings)
    weather_opening = random.choice(weather_openings)
    value_prop = random.choice(value_props)
    cta = random.choice(ctas)
    closing = random.choice(closings)
    
    # Generate insight-based message
    insight_message = ""
    for insight_key, templates in insight_templates.items():
        if insight_key in insights.lower():
            insight_message = random.choice(templates)
            break
    
    # Fallback if no specific insight matches
    if not insight_message:
        insight_message = f"I noticed {company} manages properties in {city} — that's a great opportunity for resident engagement and operational efficiency."
    
    # Construct the full message
    message = f"""{greeting}

{weather_opening}

{insight_message}

{value_prop}

{cta}

{closing}"""
    
    return message

def generate_alternative_messages(name, company, city, weather_description, insights, count=3):
    """
    Generate multiple alternative outreach messages
    
    Args:
        name (str): Lead's name
        company (str): Company name
        city (str): City name
        weather_description (str): Weather description
        insights (str): Generated insights about the area
        count (int): Number of alternative messages to generate
    
    Returns:
        list: List of alternative outreach messages
    """
    messages = []
    
    for _ in range(count):
        message = generate_outreach_message(name, company, city, weather_description, insights)
        messages.append(message)
    
    return messages

def get_message_templates():
    """
    Get available message templates and their characteristics
    
    Returns:
        dict: Message templates and their descriptions
    """
    return {
        'casual': {
            'greeting': 'Hi {name},',
            'tone': 'Friendly and approachable',
            'use_case': 'For smaller companies or personal connections'
        },
        'professional': {
            'greeting': 'Hello {name},',
            'tone': 'Formal and business-focused',
            'use_case': 'For larger companies or formal business contexts'
        },
        'warm': {
            'greeting': 'Hi there {name},',
            'tone': 'Warm and personal',
            'use_case': 'For established relationships or warm leads'
        }
    }

def analyze_message_effectiveness(message):
    """
    Analyze the effectiveness of an outreach message
    
    Args:
        message (str): The outreach message to analyze
    
    Returns:
        dict: Analysis results
    """
    analysis = {
        'length': len(message),
        'word_count': len(message.split()),
        'has_personalization': False,
        'has_value_proposition': False,
        'has_call_to_action': False,
        'tone_score': 0
    }
    
    # Check for personalization elements
    personalization_keywords = ['weather', 'city', 'company', 'area', 'market']
    analysis['has_personalization'] = any(keyword in message.lower() for keyword in personalization_keywords)
    
    # Check for value proposition
    value_keywords = ['help', 'automate', 'save time', 'improve', 'streamline', 'benefit']
    analysis['has_value_proposition'] = any(keyword in message.lower() for keyword in value_keywords)
    
    # Check for call to action
    cta_keywords = ['chat', 'call', 'schedule', 'discuss', 'explore', 'connect']
    analysis['has_call_to_action'] = any(keyword in message.lower() for keyword in cta_keywords)
    
    # Calculate tone score (simplified)
    positive_words = ['great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'perfect']
    negative_words = ['problem', 'issue', 'difficult', 'challenge', 'struggle']
    
    positive_count = sum(1 for word in positive_words if word in message.lower())
    negative_count = sum(1 for word in negative_words if word in message.lower())
    
    analysis['tone_score'] = positive_count - negative_count
    
    return analysis
