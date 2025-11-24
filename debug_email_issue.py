#!/usr/bin/env python3
"""
Debug script to identify email functionality issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.gmail_web_sender import GmailWebSender
import time

def test_gmail_web_functionality():
    print("🔍 Debugging Gmail Web Email Functionality")
    print("=" * 50)
    
    # Test data
    test_lead = {
        'name': 'Test User',
        'email': 'test@example.com',
        'company': 'Test Company',
        'city': 'Test City',
        'score': 85,
        'score_category': '🟢 High'
    }
    
    test_message = "This is a test outreach message for debugging purposes."
    
    print("1. Creating Gmail Web sender...")
    try:
        gmail_sender = GmailWebSender()
        print("✅ Gmail Web sender created successfully")
    except Exception as e:
        print(f"❌ Error creating Gmail Web sender: {e}")
        return
    
    print("\n2. Testing email content creation...")
    try:
        subject, body = gmail_sender.create_email_content(test_lead, test_message)
        print(f"✅ Email content created successfully")
        print(f"   Subject: {subject}")
        print(f"   Body length: {len(body)} characters")
    except Exception as e:
        print(f"❌ Error creating email content: {e}")
        return
    
    print("\n3. Testing URL encoding...")
    try:
        import urllib.parse
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body)
        print(f"✅ URL encoding successful")
        print(f"   Encoded subject length: {len(subject_encoded)}")
        print(f"   Encoded body length: {len(body_encoded)}")
    except Exception as e:
        print(f"❌ Error in URL encoding: {e}")
        return
    
    print("\n4. Testing Gmail URL construction...")
    try:
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={test_lead['email']}&su={subject_encoded}&body={body_encoded}"
        print(f"✅ Gmail URL constructed successfully")
        print(f"   URL length: {len(gmail_url)} characters")
        
        # Check if URL is too long (Gmail has limits)
        if len(gmail_url) > 2000:
            print(f"⚠️  WARNING: URL is very long ({len(gmail_url)} chars). This might cause issues.")
    except Exception as e:
        print(f"❌ Error constructing Gmail URL: {e}")
        return
    
    print("\n5. Testing webbrowser module...")
    try:
        import webbrowser
        print(f"✅ webbrowser module imported successfully")
        print(f"   Default browser: {webbrowser.get().name}")
    except Exception as e:
        print(f"❌ Error with webbrowser module: {e}")
        return
    
    print("\n6. Testing webbrowser.open() with timeout...")
    try:
        import webbrowser
        import threading
        import time
        
        def open_browser_with_timeout():
            try:
                webbrowser.open("https://www.google.com")
                print("✅ Browser opened successfully (test URL)")
            except Exception as e:
                print(f"❌ Error opening browser: {e}")
        
        # Run browser test in separate thread with timeout
        browser_thread = threading.Thread(target=open_browser_with_timeout)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Wait for browser to open (max 5 seconds)
        browser_thread.join(timeout=5)
        
        if browser_thread.is_alive():
            print("⚠️  Browser opening is taking longer than expected")
        else:
            print("✅ Browser test completed")
            
    except Exception as e:
        print(f"❌ Error in browser test: {e}")
        return
    
    print("\n7. Testing full Gmail compose function...")
    try:
        print("   This will attempt to open Gmail (you can cancel if needed)...")
        time.sleep(2)  # Give user time to read
        
        success, message = gmail_sender.open_gmail_compose(test_lead, test_message)
        
        if success:
            print(f"✅ Gmail compose function successful: {message}")
        else:
            print(f"❌ Gmail compose function failed: {message}")
            
    except Exception as e:
        print(f"❌ Error in Gmail compose function: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎯 Debug Summary:")
    print("If the email functionality is hanging, it's likely due to:")
    print("1. Browser not responding to webbrowser.open()")
    print("2. Gmail URL being too long")
    print("3. Network connectivity issues")
    print("4. Browser security settings blocking the request")

if __name__ == "__main__":
    test_gmail_web_functionality()


