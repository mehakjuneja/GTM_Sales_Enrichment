"""
Clay API Integration
Handles enrichment data from Clay platform
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class ClayIntegration:
    """Integration class for Clay enrichment platform"""
    
    def __init__(self, api_key: Optional[str] = None, workspace_id: Optional[str] = None):
        """
        Initialize Clay integration
        
        Args:
            api_key: Clay API key (defaults to CLAY_API_KEY env var)
            workspace_id: Clay workspace ID (defaults to CLAY_WORKSPACE_ID env var)
        """
        self.api_key = api_key or os.getenv('CLAY_API_KEY')
        self.workspace_id = workspace_id or os.getenv('CLAY_WORKSPACE_ID')
        
        if not self.api_key:
            raise ValueError("Clay API key is required. Set CLAY_API_KEY in .env file.")
        
        self.base_url = "https://api.clay.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def enrich_company(self, company_name: str, domain: Optional[str] = None,
                      location: Optional[str] = None) -> Dict:
        """
        Enrich company data via Clay
        
        Args:
            company_name: Name of the company
            domain: Company domain/website (optional)
            location: Company location (optional)
        
        Returns:
            dict: Enriched company data
        """
        url = f"{self.base_url}/enrichment/company"
        
        payload = {
            "company_name": company_name
        }
        
        if domain:
            payload["domain"] = domain
        if location:
            payload["location"] = location
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Clay company enrichment failed: {e}")
            return {}
    
    def enrich_contact(self, email: Optional[str] = None, name: Optional[str] = None,
                       company: Optional[str] = None) -> Dict:
        """
        Enrich contact data via Clay
        
        Args:
            email: Email address
            name: Full name
            company: Company name
        
        Returns:
            dict: Enriched contact data
        """
        url = f"{self.base_url}/enrichment/person"
        
        payload = {}
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name
        if company:
            payload["company"] = company
        
        if not payload:
            raise ValueError("At least one of email, name, or company must be provided")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Clay contact enrichment failed: {e}")
            return {}
    
    def bulk_enrich(self, leads: List[Dict]) -> List[Dict]:
        """
        Bulk enrich multiple leads
        
        Args:
            leads: List of lead dictionaries with company/contact info
        
        Returns:
            list: List of enriched lead dictionaries
        """
        enriched_leads = []
        
        for lead in leads:
            enriched_lead = lead.copy()
            
            # Enrich company if available
            if lead.get('company'):
                company_data = self.enrich_company(
                    company_name=lead.get('company'),
                    domain=lead.get('website'),
                    location=f"{lead.get('city', '')}, {lead.get('state', '')}"
                )
                enriched_lead['clay_company_data'] = company_data
            
            # Enrich contact if email available
            if lead.get('email'):
                contact_data = self.enrich_contact(
                    email=lead.get('email'),
                    name=lead.get('name'),
                    company=lead.get('company')
                )
                enriched_lead['clay_contact_data'] = contact_data
            
            enriched_leads.append(enriched_lead)
        
        return enriched_leads
    
    def get_clay_table_data(self, table_name: str, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve data from Clay table
        
        Args:
            table_name: Name of the Clay table
            filters: Optional filters for querying
        
        Returns:
            list: List of records from the table
        """
        url = f"{self.base_url}/tables/{table_name}/rows"
        
        params = {}
        if filters:
            params.update(filters)
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Clay table retrieval failed: {e}")
            return []
    
    def update_clay_table(self, table_name: str, data: List[Dict]) -> Dict:
        """
        Update Clay table with enrichment results
        
        Args:
            table_name: Name of the Clay table
            data: List of dictionaries containing data to update
        
        Returns:
            dict: Response from Clay API
        """
        url = f"{self.base_url}/tables/{table_name}/rows"
        
        payload = {
            "rows": data
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Clay table update failed: {e}")
            return {}
    
    def enrich_with_clay_insights(self, lead_data: Dict) -> Dict:
        """
        Enhance lead data with Clay insights
        
        Args:
            lead_data: Dictionary containing basic lead information
        
        Returns:
            dict: Enhanced lead data with Clay insights
        """
        enhanced_data = lead_data.copy()
        
        # Enrich company
        if lead_data.get('company'):
            company_data = self.enrich_company(
                company_name=lead_data.get('company'),
                domain=lead_data.get('website'),
                location=f"{lead_data.get('city', '')}, {lead_data.get('state', '')}"
            )
            
            # Extract useful company insights
            if company_data:
                enhanced_data['clay_employee_count'] = company_data.get('employee_count')
                enhanced_data['clay_revenue'] = company_data.get('revenue')
                enhanced_data['clay_industry'] = company_data.get('industry')
                enhanced_data['clay_funding'] = company_data.get('total_funding')
                enhanced_data['clay_technologies'] = company_data.get('technologies', [])
                enhanced_data['clay_linkedin_url'] = company_data.get('linkedin_url')
        
        # Enrich contact
        if lead_data.get('email'):
            contact_data = self.enrich_contact(
                email=lead_data.get('email'),
                name=lead_data.get('name'),
                company=lead_data.get('company')
            )
            
            # Extract useful contact insights
            if contact_data:
                enhanced_data['clay_job_title'] = contact_data.get('job_title')
                enhanced_data['clay_linkedin_profile'] = contact_data.get('linkedin_url')
                enhanced_data['clay_social_profiles'] = contact_data.get('social_profiles', [])
        
        return enhanced_data
    
    def get_enrichment_status(self, enrichment_id: str) -> Dict:
        """
        Check status of an enrichment job
        
        Args:
            enrichment_id: ID of the enrichment job
        
        Returns:
            dict: Status information
        """
        url = f"{self.base_url}/enrichment/{enrichment_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Clay enrichment status check failed: {e}")
            return {}

