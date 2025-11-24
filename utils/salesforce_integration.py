"""
Salesforce CRM Integration
Handles bidirectional sync between lead enrichment system and Salesforce
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

try:
    from simple_salesforce import Salesforce
    SALESFORCE_AVAILABLE = True
except ImportError:
    SALESFORCE_AVAILABLE = False
    print("Warning: simple-salesforce not installed. Install with: pip install simple-salesforce")

load_dotenv()

class SalesforceIntegration:
    """Integration class for Salesforce CRM"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None,
                 security_token: Optional[str] = None, domain: str = "login"):
        """
        Initialize Salesforce integration
        
        Args:
            username: Salesforce username (defaults to SALESFORCE_USERNAME env var)
            password: Salesforce password (defaults to SALESFORCE_PASSWORD env var)
            security_token: Salesforce security token (defaults to SALESFORCE_SECURITY_TOKEN env var)
            domain: Salesforce domain (login for production, test for sandbox)
        """
        if not SALESFORCE_AVAILABLE:
            raise ImportError("simple-salesforce package is required. Install with: pip install simple-salesforce")
        
        self.username = username or os.getenv('SALESFORCE_USERNAME')
        self.password = password or os.getenv('SALESFORCE_PASSWORD')
        self.security_token = security_token or os.getenv('SALESFORCE_SECURITY_TOKEN')
        self.domain = domain
        
        if not all([self.username, self.password, self.security_token]):
            raise ValueError("Salesforce credentials are required. Set SALESFORCE_USERNAME, SALESFORCE_PASSWORD, and SALESFORCE_SECURITY_TOKEN in .env file.")
        
        # Initialize Salesforce connection
        self.sf = Salesforce(
            username=self.username,
            password=self.password,
            security_token=self.security_token,
            domain=self.domain
        )
    
    def create_custom_fields(self) -> Dict:
        """
        Create custom fields in Salesforce for enrichment data
        Note: This requires Metadata API access and is complex.
        For now, this is a placeholder - fields should be created manually in Salesforce Setup.
        
        Returns:
            dict: Instructions for manual field creation
        """
        return {
            "message": "Custom fields should be created manually in Salesforce Setup",
            "required_fields": [
                {
                    "name": "Enrichment_Lead_Score__c",
                    "type": "Number",
                    "label": "Lead Score",
                    "description": "Lead score calculated by enrichment system (0-100)",
                    "precision": 0,
                    "scale": 0
                },
                {
                    "name": "Enrichment_Score_Category__c",
                    "type": "Picklist",
                    "label": "Score Category",
                    "values": ["High", "Medium", "Low"]
                },
                {
                    "name": "Enrichment_Temperature__c",
                    "type": "Number",
                    "label": "Temperature",
                    "description": "Current temperature in area"
                },
                {
                    "name": "Enrichment_Weather_Description__c",
                    "type": "Text",
                    "label": "Weather Description",
                    "length": 255
                },
                {
                    "name": "Enrichment_Median_Income__c",
                    "type": "Currency",
                    "label": "Median Income"
                },
                {
                    "name": "Enrichment_Percent_Renters__c",
                    "type": "Percent",
                    "label": "Percent Renters"
                },
                {
                    "name": "Enrichment_Population__c",
                    "type": "Number",
                    "label": "Population"
                },
                {
                    "name": "Enrichment_Insights__c",
                    "type": "Long Text Area",
                    "label": "Market Insights",
                    "length": 32768
                },
                {
                    "name": "Enrichment_Outreach_Message__c",
                    "type": "Long Text Area",
                    "label": "Outreach Message",
                    "length": 32768
                },
                {
                    "name": "Enrichment_Enriched_At__c",
                    "type": "DateTime",
                    "label": "Enriched At"
                },
                {
                    "name": "Enrichment_Enrichment_Status__c",
                    "type": "Picklist",
                    "label": "Enrichment Status",
                    "values": ["Success", "Failed", "Pending"]
                }
            ]
        }
    
    def sync_lead_to_salesforce(self, lead_data: Dict, record_id: Optional[str] = None,
                                record_type: str = "Lead") -> Dict:
        """
        Push enriched lead data to Salesforce
        
        Args:
            lead_data: Dictionary containing enriched lead data
            record_id: Existing Salesforce record ID (optional)
            record_type: Type of record (Lead or Contact)
        
        Returns:
            dict: Response from Salesforce API
        """
        # Map enrichment data to Salesforce fields
        fields = {
            "Enrichment_Lead_Score__c": lead_data.get('score'),
            "Enrichment_Score_Category__c": lead_data.get('score_category', '').replace('🟢 ', '').replace('🟡 ', '').replace('🔴 ', ''),
            "Enrichment_Temperature__c": lead_data.get('temperature'),
            "Enrichment_Weather_Description__c": lead_data.get('weather_description'),
            "Enrichment_Median_Income__c": lead_data.get('median_income'),
            "Enrichment_Percent_Renters__c": lead_data.get('percent_renters'),
            "Enrichment_Population__c": lead_data.get('population'),
            "Enrichment_Insights__c": lead_data.get('insights'),
            "Enrichment_Outreach_Message__c": lead_data.get('outreach_message'),
            "Enrichment_Enriched_At__c": datetime.now().isoformat(),
            "Enrichment_Enrichment_Status__c": "Success"
        }
        
        # Also update standard fields if available
        if lead_data.get('email'):
            fields['Email'] = lead_data.get('email')
        if lead_data.get('name'):
            name_parts = lead_data.get('name', '').split()
            if len(name_parts) > 0:
                fields['FirstName'] = name_parts[0]
            if len(name_parts) > 1:
                fields['LastName'] = ' '.join(name_parts[1:])
        if lead_data.get('company'):
            fields['Company'] = lead_data.get('company')
        if lead_data.get('city'):
            fields['City'] = lead_data.get('city')
        if lead_data.get('state'):
            fields['State'] = lead_data.get('state')
        if lead_data.get('country'):
            fields['Country'] = lead_data.get('country')
        
        # Remove None values
        fields = {k: v for k, v in fields.items() if v is not None}
        
        if record_id:
            # Update existing record
            result = getattr(self.sf, record_type).update(record_id, fields)
        else:
            # Create new record
            result = getattr(self.sf, record_type).create(fields)
        
        return result
    
    def get_salesforce_leads(self, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """
        Pull leads from Salesforce for enrichment
        
        Args:
            filters: Optional SOQL WHERE clause filters
            limit: Maximum number of records to retrieve
        
        Returns:
            list: List of lead dictionaries
        """
        # Build SOQL query
        fields = [
            "Id", "Email", "FirstName", "LastName", "Company", 
            "City", "State", "Country", "Enrichment_Enriched_At__c"
        ]
        
        query = f"SELECT {', '.join(fields)} FROM Lead"
        
        # Add filters
        if filters:
            where_clauses = []
            for key, value in filters.items():
                if value is None:
                    where_clauses.append(f"{key} = null")
                else:
                    where_clauses.append(f"{key} = '{value}'")
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += f" LIMIT {limit}"
        
        # Execute query
        results = self.sf.query(query)
        return results.get('records', [])
    
    def update_salesforce_record(self, record_id: str, record_type: str, fields: Dict) -> Dict:
        """
        Update Salesforce record with enrichment data
        
        Args:
            record_id: Salesforce record ID
            record_type: Type of record (Lead, Contact, etc.)
            fields: Dictionary of fields to update
        
        Returns:
            dict: Response from Salesforce API
        """
        # Remove None values
        fields = {k: v for k, v in fields.items() if v is not None}
        
        result = getattr(self.sf, record_type).update(record_id, fields)
        return result
    
    def create_task(self, record_id: str, record_type: str, task_data: Dict) -> Dict:
        """
        Create follow-up task in Salesforce
        
        Args:
            record_id: Salesforce record ID to associate task with
            record_type: Type of record (Lead, Contact, etc.)
            task_data: Dictionary containing task information
        
        Returns:
            dict: Response from Salesforce API
        """
        task_fields = {
            "Subject": task_data.get('subject', 'Follow up on enriched lead'),
            "Status": task_data.get('status', 'Not Started'),
            "Priority": task_data.get('priority', 'Normal'),
            "Description": task_data.get('description', ''),
            "WhatId": record_id,  # Associate with the record
            "ActivityDate": task_data.get('due_date', datetime.now().date().isoformat())
        }
        
        result = self.sf.Task.create(task_fields)
        return result
    
    def search_by_email(self, email: str, record_type: str = "Lead") -> Optional[Dict]:
        """
        Search for record by email address
        
        Args:
            email: Email address to search for
            record_type: Type of record to search (Lead or Contact)
        
        Returns:
            dict: Record data if found, None otherwise
        """
        query = f"SELECT Id, Email, FirstName, LastName, Company FROM {record_type} WHERE Email = '{email}' LIMIT 1"
        
        try:
            results = self.sf.query(query)
            records = results.get('records', [])
            if records:
                return records[0]
            return None
        except Exception:
            return None
    
    def bulk_sync_leads(self, leads: List[Dict], record_type: str = "Lead") -> Dict:
        """
        Bulk sync multiple leads to Salesforce
        
        Args:
            leads: List of lead dictionaries
            record_type: Type of record (Lead or Contact)
        
        Returns:
            dict: Summary of sync results
        """
        results = {
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        for lead in leads:
            try:
                # Check if record exists
                record_id = None
                if lead.get('email'):
                    existing = self.search_by_email(lead['email'], record_type)
                    if existing:
                        record_id = existing['Id']
                
                # Sync lead
                self.sync_lead_to_salesforce(lead, record_id, record_type)
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "lead": lead.get('email', 'Unknown'),
                    "error": str(e)
                })
        
        return results

