#!/usr/bin/env python3
"""
Quick email setup test script
"""

import os
from dotenv import load_dotenv
from utils.email_sender import EmailSender, test_email_configuration, send_test_email

def main():
    print("🧪 EliseAI Email Setup Test")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check configuration
    print("1. Checking email configuration...")
    sender = EmailSender()
    config_status = sender.get_email_config_status()
    
    if config_status['configured']:
        print("✅ Email configuration found!")
        print(f"   Sender: {config_status['sender_name']} <{config_status['sender_email']}>")
        print(f"   SMTP: {config_status['smtp_server']}:{config_status['smtp_port']}")
    else:
        print("❌ Email not configured!")
        print("   Missing:", ", ".join(config_status['missing_config']))
        print("\n   Please edit your .env file with:")
        print("   SENDER_EMAIL=your_email@gmail.com")
        print("   SENDER_PASSWORD=your_app_password")
        print("   SENDER_NAME=EliseAI Sales Team")
        return
    
    # Test configuration
    print("\n2. Testing email configuration...")
    success, message = test_email_configuration()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return
    
    # Send test email
    print("\n3. Sending test email...")
    test_email = input("Enter your email address to receive test email: ").strip()
    
    if test_email:
        print(f"Sending test email to {test_email}...")
        success, message = send_test_email(test_email)
        
        if success:
            print(f"✅ Test email sent successfully!")
            print(f"   Check your inbox at {test_email}")
        else:
            print(f"❌ Failed to send test email: {message}")
    else:
        print("No email address provided. Skipping test email.")
    
    print("\n🎉 Email setup test complete!")
    print("\nNext steps:")
    print("1. Run the main app: ./start_app.sh")
    print("2. Go to Settings page to test email configuration")
    print("3. Go to Dashboard to send emails to high-priority leads")

if __name__ == "__main__":
    main()
