#!/bin/bash

# EliseAI Lead Enrichment App Startup Script

echo "🏠 Starting EliseAI Lead Enrichment & Outreach Assistant..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found."
    echo "   Please create a .env file with your API keys:"
    echo "   OPENWEATHER_API_KEY=your_key_here"
    echo "   DATAUSA_API_KEY=your_key_here"
    echo "   OPENAI_API_KEY=your_key_here"
    echo ""
    echo "   For email functionality, also add:"
    echo "   SENDER_EMAIL=your_email@gmail.com"
    echo "   SENDER_PASSWORD=your_app_password"
    echo "   SENDER_NAME=EliseAI Sales Team"
    echo ""
    echo "   The app will work with mock data if no API keys are provided."
    echo ""
fi

# Check if Python dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import streamlit, pandas, requests, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "🚀 Starting Streamlit app..."
echo "   The app will open in your default web browser."
echo "   Press Ctrl+C to stop the app."
echo ""

# Start the Streamlit app
streamlit run app.py
