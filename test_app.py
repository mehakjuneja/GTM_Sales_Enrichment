#!/usr/bin/env python3
"""
Test script for EliseAI Lead Enrichment App
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from utils.api_calls import enrich_lead_data, get_mock_data
        from utils.scoring import calculate_lead_score, categorize_score
        from utils.outreach import generate_outreach_message
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_scoring():
    """Test the scoring algorithm"""
    try:
        from utils.scoring import calculate_lead_score, categorize_score
        
        # Test case 1: High score scenario
        score1 = calculate_lead_score(60, 80000, 75)  # High renters, high income, good temp
        category1 = categorize_score(score1)
        print(f"✅ High score test: {score1} ({category1})")
        
        # Test case 2: Low score scenario
        score2 = calculate_lead_score(20, 40000, 95)  # Low renters, low income, hot temp
        category2 = categorize_score(score2)
        print(f"✅ Low score test: {score2} ({category2})")
        
        return True
    except Exception as e:
        print(f"❌ Scoring test error: {e}")
        return False

def test_outreach():
    """Test the outreach message generation"""
    try:
        from utils.outreach import generate_outreach_message
        
        message = generate_outreach_message(
            "John Doe", 
            "ABC Properties", 
            "San Francisco", 
            "sunny", 
            "high rental market, affluent area"
        )
        
        print("✅ Outreach message generated:")
        print(f"Length: {len(message)} characters")
        print(f"Contains name: {'John Doe' in message}")
        print(f"Contains company: {'ABC Properties' in message}")
        
        return True
    except Exception as e:
        print(f"❌ Outreach test error: {e}")
        return False

def test_mock_data():
    """Test the mock data generation"""
    try:
        from utils.api_calls import get_mock_data
        
        mock_data = get_mock_data("Test City", "Test State", "Test Country")
        
        required_fields = ['temperature', 'weather_description', 'population', 'median_income', 'percent_renters']
        missing_fields = [field for field in required_fields if field not in mock_data]
        
        if missing_fields:
            print(f"❌ Mock data missing fields: {missing_fields}")
            return False
        
        print("✅ Mock data generation successful")
        print(f"Sample data: {mock_data}")
        
        return True
    except Exception as e:
        print(f"❌ Mock data test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing EliseAI Lead Enrichment App")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Scoring Test", test_scoring),
        ("Outreach Test", test_outreach),
        ("Mock Data Test", test_mock_data),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("\nTo start the app, run:")
        print("streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
