#!/usr/bin/env python3
"""
Simple email test without external dependencies
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email():
    print("🧪 Simple Email Test for mehakjuneja12@gmail.com")
    print("=" * 50)
    
    # Email configuration
    sender_email = "mehakjuneja12@gmail.com"
    sender_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    if not sender_password:
        print("❌ No password provided. Exiting.")
        return
    
    # Test recipient (send to yourself)
    recipient_email = input("Enter recipient email (or press Enter to send to yourself): ").strip()
    if not recipient_email:
        recipient_email = sender_email
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "EliseAI Email Test - Lead Enrichment App"
        
        # Email body
        body = """
Hello!

This is a test email from the EliseAI Lead Enrichment App.

If you received this email, your email configuration is working correctly!

Features tested:
✅ SMTP connection to Gmail
✅ Email authentication
✅ Message sending

This confirms that the automated email campaigns for high-priority leads will work properly.

Best regards,
EliseAI Sales Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print(f"📧 Sending test email to {recipient_email}...")
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print("✅ Test email sent successfully!")
        print(f"   Check your inbox at {recipient_email}")
        print("\n🎉 Email setup is working! You can now use the email functionality in the app.")
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're using an App Password, not your regular Gmail password")
        print("2. Enable 2-Factor Authentication in your Google Account")
        print("3. Generate a new App Password if needed")

if __name__ == "__main__":
    test_email()
