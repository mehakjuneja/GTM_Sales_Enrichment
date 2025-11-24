#!/usr/bin/env python3
"""
Test Gmail Web integration
"""

from utils.gmail_web_sender import GmailWebSender

def main():
    print("🌐 Gmail Web Test")
    print("=" * 40)
    
    # Create test lead data
    test_lead = {
        'name': 'Mehak Juneja',
        'email': 'mehakjuneja12@gmail.com',
        'company': 'Demo Company',
        'city': 'San Francisco',
        'score': 85,
        'score_category': '🟢 High'
    }
    
    test_message = """I hope this message finds you well. I'm reaching out because I noticed that Demo Company manages properties in San Francisco - an area we've identified as having excellent potential for our property management solutions.

Market Score: 85/100 (High Priority)

San Francisco is a premium rental market with high-income residents and optimal weather conditions, making it an ideal location for our property management services.

This is a test email to demonstrate the Gmail web integration functionality."""
    
    print("Creating Gmail Web sender...")
    gmail_sender = GmailWebSender()
    
    print("Opening Gmail web interface with test email...")
    print("This will open Gmail in your web browser with a pre-composed email.")
    
    success, message = gmail_sender.open_gmail_compose(test_lead, test_message)
    
    if success:
        print(f"✅ {message}")
        print("\n🎉 Gmail should have opened in your browser with your test email!")
        print("You can now:")
        print("1. Review the pre-composed email in Gmail")
        print("2. Make any edits if needed")
        print("3. Send the email directly from Gmail")
        print("4. Use this feature in the main app for real leads")
    else:
        print(f"❌ {message}")
    
    print("\nTo use this in the main app:")
    print("1. Run: ./start_app.sh")
    print("2. Go to Dashboard page")
    print("3. Select 'Gmail Web (Recommended)'")
    print("4. Click 'Test Gmail Web' or 'Open Gmail for All High-Priority Leads'")
    
    print("\nAdditional features:")
    print("- Click 'Open Gmail Inbox' to open your Gmail inbox")
    print("- Use 'Preview Email Template' to see what emails will look like")

if __name__ == "__main__":
    main()
