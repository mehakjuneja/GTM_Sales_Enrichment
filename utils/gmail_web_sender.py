"""
Gmail Web integration for Lead Enrichment App
Opens Gmail web interface with pre-composed emails for leads
"""

import webbrowser
import urllib.parse
from datetime import datetime

class GmailWebSender:
    """Handle opening Gmail web interface with pre-composed emails"""
    
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
    
    def open_gmail_compose(self, lead_data, outreach_message):
        """Open Gmail web interface with pre-composed email"""
        
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
            
            # Create Gmail compose URL
            gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient_email}&su={subject_encoded}&body={body_encoded}"
            
            # Open Gmail in web browser
            webbrowser.open(gmail_url)
            
            return True, f"Gmail opened with email to {recipient_email}"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def open_bulk_gmail_emails(self, leads_df, min_score=71):
        """Open Gmail for multiple high-priority leads"""
        
        # Filter high-priority leads
        high_priority_leads = leads_df[leads_df['score'] >= min_score].copy()
        
        if high_priority_leads.empty:
            return False, f"No leads found with score >= {min_score}"
        
        results = []
        successful_opens = 0
        failed_opens = 0
        
        for idx, lead in high_priority_leads.iterrows():
            try:
                success, message = self.open_gmail_compose(lead.to_dict(), lead.get('outreach_message', ''))
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
        summary = f"Gmail opened for {successful_opens} leads, {failed_opens} failed"
        
        return True, {
            'summary': summary,
            'successful_opens': successful_opens,
            'failed_opens': failed_opens,
            'total_leads': len(high_priority_leads),
            'results': results
        }
    
    def preview_email(self, lead_data, outreach_message):
        """Preview email content without opening Gmail"""
        
        subject, body = self.create_email_content(lead_data, outreach_message)
        
        return {
            'to': lead_data.get('email', 'No email'),
            'subject': subject,
            'body': body,
            'lead_name': lead_data.get('name', 'Unknown'),
            'company': lead_data.get('company', 'Unknown'),
            'score': lead_data.get('score', 0)
        }
    
    def open_gmail_inbox(self):
        """Open Gmail inbox"""
        try:
            webbrowser.open("https://mail.google.com")
            return True, "Gmail inbox opened"
        except Exception as e:
            return False, f"Error opening Gmail: {str(e)}"

def test_gmail_web():
    """Test Gmail web functionality"""
    
    # Create test lead data
    test_lead = {
        'name': 'Test User',
        'email': 'mehakjuneja12@gmail.com',  # Send to yourself for testing
        'company': 'Test Company',
        'city': 'Test City',
        'score': 85,
        'score_category': '🟢 High'
    }
    
    test_message = """I hope this message finds you well. I'm reaching out because I noticed that Test Company manages properties in Test City - an area we've identified as having excellent potential for our property management solutions.

Market Score: 85/100 (High Priority)

Test City is a premium rental market with high-income residents and optimal weather conditions, making it an ideal location for our property management services.

This is a test email to demonstrate the Gmail web integration functionality."""
    
    sender = GmailWebSender()
    return sender.open_gmail_compose(test_lead, test_message)
