"""
Mac Mail App integration for Lead Enrichment App
Opens Mac's Mail app with pre-composed emails for leads
"""

import subprocess
import urllib.parse
from datetime import datetime

class MailAppSender:
    """Handle opening Mac Mail app with pre-composed emails"""
    
    def __init__(self):
        self.sender_name = "Sales Team"
        self.sender_email = "mehakjuneja12@gmail.com"  # Your email
    
    def create_email_content(self, lead_data, outreach_message):
        """Create email content for the lead"""
        
        # Extract lead information
        name = lead_data.get('name', 'Valued Customer')
        company = lead_data.get('company', 'Your Company')
        city = lead_data.get('city', 'Your City')
        score = lead_data.get('score', 0)
        score_category = lead_data.get('score_category', 'Medium')
        
        # Create subject line
        subject = f"Property Management Solutions for {company} in {city}"
        
        # Create email body - outreach message already contains greeting
        email_body = f"""{outreach_message}

---
This email was sent because your company was identified as a high-priority lead for our property management services.
If you'd prefer not to receive these emails, please reply with "UNSUBSCRIBE" and we'll remove you from our list.
        """
        
        return subject, email_body
    
    def open_mail_app(self, lead_data, outreach_message):
        """Open Mac Mail app with pre-composed email"""
        
        try:
            # Get email content
            subject, body = self.create_email_content(lead_data, outreach_message)
            
            # Get recipient email
            recipient_email = lead_data.get('email', '')
            if not recipient_email:
                return False, "No email address found for this lead"
            
            # URL encode the content
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)
            
            # Create mailto URL
            mailto_url = f"mailto:{recipient_email}?subject={subject_encoded}&body={body_encoded}"
            
            # Open Mail app with the pre-composed email
            subprocess.run(['open', mailto_url], check=True)
            
            return True, f"Mail app opened with email to {recipient_email}"
            
        except subprocess.CalledProcessError:
            return False, "Failed to open Mail app"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def open_bulk_emails(self, leads_df, min_score=71):
        """Open Mail app for multiple high-priority leads"""
        
        # Filter high-priority leads
        high_priority_leads = leads_df[leads_df['score'] >= min_score].copy()
        
        if high_priority_leads.empty:
            return False, f"No leads found with score >= {min_score}"
        
        results = []
        successful_opens = 0
        failed_opens = 0
        
        for idx, lead in high_priority_leads.iterrows():
            try:
                success, message = self.open_mail_app(lead.to_dict(), lead.get('outreach_message', ''))
                results.append({
                    'name': lead.get('name'),
                    'email': lead.get('email'),
                    'company': lead.get('company'),
                    'score': lead.get('score'),
                    'success': success,
                    'message': message
                })
                
                if success:
                    successful_opens += 1
                else:
                    failed_opens += 1
                    
            except Exception as e:
                results.append({
                    'name': lead.get('name'),
                    'email': lead.get('email'),
                    'company': lead.get('company'),
                    'score': lead.get('score'),
                    'success': False,
                    'message': f"Error: {str(e)}"
                })
                failed_opens += 1
        
        # Create summary
        summary = f"Mail app opened for {successful_opens} leads, {failed_opens} failed"
        
        return True, {
            'summary': summary,
            'successful_opens': successful_opens,
            'failed_opens': failed_opens,
            'total_leads': len(high_priority_leads),
            'results': results
        }
    
    def preview_email(self, lead_data, outreach_message):
        """Preview email content without opening Mail app"""
        
        subject, body = self.create_email_content(lead_data, outreach_message)
        
        return {
            'to': lead_data.get('email', 'No email'),
            'subject': subject,
            'body': body,
            'lead_name': lead_data.get('name', 'Unknown'),
            'company': lead_data.get('company', 'Unknown'),
            'score': lead_data.get('score', 0)
        }

def test_mail_app():
    """Test Mail app functionality"""
    
    # Create test lead data
    test_lead = {
        'name': 'Test User',
        'email': 'mehakjuneja12@gmail.com',  # Send to yourself for testing
        'company': 'Test Company',
        'city': 'Test City',
        'score': 85,
        'score_category': '🟢 High'
    }
    
    test_message = """
This is a test email from the Lead Enrichment App.

If you received this email, the Mail app integration is working correctly!

This is a test of our automated outreach system for high-priority leads.
    """
    
    sender = MailAppSender()
    return sender.open_mail_app(test_lead, test_message)
