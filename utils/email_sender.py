"""
Email functionality for Lead Enrichment App
Handles automated email sending to high-priority leads
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSender:
    """Handle email sending functionality for high-priority leads"""
    
    def __init__(self):
        """Initialize email sender with SMTP configuration"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.sender_name = os.getenv('SENDER_NAME', 'Sales Team')
        
    def is_configured(self):
        """Check if email is properly configured"""
        return bool(self.sender_email and self.sender_password)
    
    def create_email_template(self, lead_data, outreach_message):
        """Create HTML email template for lead outreach"""
        
        # Extract lead information
        name = lead_data.get('name', 'Valued Customer')
        company = lead_data.get('company', 'Your Company')
        city = lead_data.get('city', 'Your City')
        score = lead_data.get('score', 0)
        score_category = lead_data.get('score_category', 'Medium')
        
        # Create HTML email template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                    text-align: center;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .score-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .score-high {{
                    background: #4CAF50;
                    color: white;
                }}
                .score-medium {{
                    background: #FF9800;
                    color: white;
                }}
                .score-low {{
                    background: #f44336;
                    color: white;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏠 Property Management Solutions</h1>
                <p>Property Management Solutions</p>
            </div>
            
            <div class="content">
                <div style="background: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    {outreach_message.replace(chr(10), '<br>')}
                </div>
            </div>
            
            <div class="footer">
                <p>This email was sent to {lead_data.get('email', 'your email')} because your company was identified as a high-potential lead for our property management services.</p>
                <p>If you'd prefer not to receive these emails, please reply with "UNSUBSCRIBE" and we'll remove you from our list.</p>
                <p>Property Management Solutions | {datetime.now().year}</p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def send_lead_email(self, lead_data, outreach_message, recipient_email=None):
        """Send email to a specific lead"""
        
        if not self.is_configured():
            raise Exception("Email not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file")
        
        # Use provided email or lead's email
        email = recipient_email or lead_data.get('email')
        if not email:
            raise Exception("No email address provided")
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = email
            msg['Subject'] = f"Property Management Solutions for {lead_data.get('company', 'Your Company')} in {lead_data.get('city', 'Your City')}"
            
            # Create HTML content
            html_content = self.create_email_template(lead_data, outreach_message)
            
            # Create plain text version - outreach message already contains greeting
            text_content = f"""{outreach_message}

---
This email was sent to {email} because your company was identified as a high-potential lead for our property management services.
If you'd prefer not to receive these emails, please reply with "UNSUBSCRIBE" and we'll remove you from our list.
            """
            
            # Attach both versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True, f"Email sent successfully to {email}"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_bulk_emails(self, leads_df, min_score=71):
        """Send emails to all high-priority leads"""
        
        if not self.is_configured():
            return False, "Email not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file"
        
        # Filter high-priority leads
        high_priority_leads = leads_df[leads_df['score'] >= min_score].copy()
        
        if high_priority_leads.empty:
            return False, f"No leads found with score >= {min_score}"
        
        results = []
        successful_sends = 0
        failed_sends = 0
        
        for idx, lead in high_priority_leads.iterrows():
            try:
                success, message = self.send_lead_email(lead.to_dict(), lead.get('outreach_message', ''))
                results.append({
                    'name': lead.get('name'),
                    'email': lead.get('email'),
                    'company': lead.get('company'),
                    'score': lead.get('score'),
                    'success': success,
                    'message': message
                })
                
                if success:
                    successful_sends += 1
                else:
                    failed_sends += 1
                    
            except Exception as e:
                results.append({
                    'name': lead.get('name'),
                    'email': lead.get('email'),
                    'company': lead.get('company'),
                    'score': lead.get('score'),
                    'success': False,
                    'message': f"Error: {str(e)}"
                })
                failed_sends += 1
        
        # Create summary
        summary = f"Email campaign completed: {successful_sends} successful, {failed_sends} failed"
        
        return True, {
            'summary': summary,
            'successful_sends': successful_sends,
            'failed_sends': failed_sends,
            'total_leads': len(high_priority_leads),
            'results': results
        }
    
    def get_email_config_status(self):
        """Get email configuration status"""
        return {
            'configured': self.is_configured(),
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'sender_email': self.sender_email,
            'sender_name': self.sender_name,
            'missing_config': [] if self.is_configured() else [
                'SENDER_EMAIL' if not self.sender_email else None,
                'SENDER_PASSWORD' if not self.sender_password else None
            ]
        }

def test_email_configuration():
    """Test email configuration"""
    sender = EmailSender()
    config_status = sender.get_email_config_status()
    
    if config_status['configured']:
        return True, "Email configuration is valid"
    else:
        missing = [item for item in config_status['missing_config'] if item]
        return False, f"Missing email configuration: {', '.join(missing)}"

def send_test_email(test_email):
    """Send a test email to verify configuration"""
    sender = EmailSender()
    
    if not sender.is_configured():
        return False, "Email not configured"
    
    # Create test lead data
    test_lead = {
        'name': 'Test User',
        'company': 'Test Company',
        'city': 'Test City',
        'score': 85,
        'score_category': '🟢 High',
        'email': test_email
    }
    
    test_message = """
This is a test email from Lead Enrichment App.

If you received this email, your email configuration is working correctly!

This is a test of our automated outreach system for high-priority leads.
    """
    
    return sender.send_lead_email(test_lead, test_message, test_email)
