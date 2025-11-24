#!/usr/bin/env python3
"""
Test Mac Mail App integration
"""

from utils.mail_app_sender import MailAppSender

def main():
    print("📱 Mac Mail App Test")
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
    
    test_message = """
I hope this message finds you well. I'm reaching out because I noticed that Demo Company manages properties in San Francisco - an area we've identified as having excellent potential for our property management solutions.

Market Score: 85/100 (High Priority)

San Francisco is a premium rental market with high-income residents and optimal weather conditions, making it an ideal location for our property management services.

I'd love to schedule a brief 15-minute call to discuss how we can help streamline your property management operations and improve resident satisfaction.

This is a test email to demonstrate the Mail app integration functionality.
    """
    
    print("Creating Mail App sender...")
    mail_sender = MailAppSender()
    
    print("Opening Mail app with test email...")
    print("This will open your Mac's Mail app with a pre-composed email.")
    
    success, message = mail_sender.open_mail_app(test_lead, test_message)
    
    if success:
        print(f"✅ {message}")
        print("\n🎉 Mail app should have opened with your test email!")
        print("You can now:")
        print("1. Review the pre-composed email")
        print("2. Make any edits if needed")
        print("3. Send the email")
        print("4. Use this feature in the main app for real leads")
    else:
        print(f"❌ {message}")
    
    print("\nTo use this in the main app:")
    print("1. Run: ./start_app.sh")
    print("2. Go to Dashboard page")
    print("3. Select 'Mac Mail App (Recommended)'")
    print("4. Click 'Test Mail App' or 'Open Mail App for All High-Priority Leads'")

if __name__ == "__main__":
    main()
