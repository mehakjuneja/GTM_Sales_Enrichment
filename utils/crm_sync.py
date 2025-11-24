"""
Unified CRM Sync Module
Provides a common interface for syncing with multiple CRM systems
"""

from typing import Dict, List, Optional, Literal
from abc import ABC, abstractmethod

try:
    from .hubspot_integration import HubSpotIntegration
    HUBSPOT_AVAILABLE = True
except ImportError:
    HUBSPOT_AVAILABLE = False

try:
    from .salesforce_integration import SalesforceIntegration
    SALESFORCE_AVAILABLE = True
except ImportError:
    SALESFORCE_AVAILABLE = False

class CRMAdapter(ABC):
    """Abstract base class for CRM adapters"""
    
    @abstractmethod
    def sync_lead(self, lead_data: Dict, record_id: Optional[str] = None) -> Dict:
        """Sync lead data to CRM"""
        pass
    
    @abstractmethod
    def get_leads(self, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """Get leads from CRM"""
        pass
    
    @abstractmethod
    def update_record(self, record_id: str, fields: Dict) -> Dict:
        """Update record in CRM"""
        pass

class UnifiedCRMSync:
    """Unified interface for syncing with multiple CRM systems"""
    
    def __init__(self, crm_type: Literal['hubspot', 'salesforce'], **kwargs):
        """
        Initialize unified CRM sync
        
        Args:
            crm_type: Type of CRM ('hubspot' or 'salesforce')
            **kwargs: Additional arguments for CRM initialization
        """
        self.crm_type = crm_type.lower()
        
        if self.crm_type == 'hubspot':
            if not HUBSPOT_AVAILABLE:
                raise ImportError("HubSpot integration not available. Install required dependencies.")
            self.crm = HubSpotIntegration(**kwargs)
        elif self.crm_type == 'salesforce':
            if not SALESFORCE_AVAILABLE:
                raise ImportError("Salesforce integration not available. Install simple-salesforce.")
            self.crm = SalesforceIntegration(**kwargs)
        else:
            raise ValueError(f"Unsupported CRM type: {crm_type}. Use 'hubspot' or 'salesforce'.")
    
    def sync_enriched_lead(self, lead_data: Dict, record_id: Optional[str] = None) -> Dict:
        """
        Sync enriched lead data to CRM
        
        Args:
            lead_data: Dictionary containing enriched lead data
            record_id: Existing CRM record ID (optional)
        
        Returns:
            dict: Response from CRM API
        """
        if self.crm_type == 'hubspot':
            return self.crm.sync_lead_to_hubspot(lead_data, record_id)
        elif self.crm_type == 'salesforce':
            record_type = lead_data.get('record_type', 'Lead')
            return self.crm.sync_lead_to_salesforce(lead_data, record_id, record_type)
    
    def get_leads_for_enrichment(self, filters: Optional[Dict] = None, 
                                 limit: int = 100) -> List[Dict]:
        """
        Get leads from CRM that need enrichment
        
        Args:
            filters: Optional filters for querying
            limit: Maximum number of leads to retrieve
        
        Returns:
            list: List of lead dictionaries
        """
        if self.crm_type == 'hubspot':
            # Filter for leads that haven't been enriched
            if not filters:
                filters = {}
            filters['enrichment_enriched_at'] = {'operator': 'NOT_HAS_PROPERTY'}
            return self.crm.get_hubspot_leads(filters, limit)
        elif self.crm_type == 'salesforce':
            # Filter for leads that haven't been enriched
            if not filters:
                filters = {}
            filters['Enrichment_Enriched_At__c'] = None
            return self.crm.get_salesforce_leads(filters, limit)
    
    def update_with_enrichment(self, record_id: str, enriched_data: Dict) -> Dict:
        """
        Update CRM record with enrichment data
        
        Args:
            record_id: CRM record ID
            enriched_data: Dictionary containing enrichment data
        
        Returns:
            dict: Response from CRM API
        """
        # Map enriched data to CRM fields
        if self.crm_type == 'hubspot':
            properties = {
                "enrichment_lead_score": enriched_data.get('score'),
                "enrichment_score_category": enriched_data.get('score_category', '').replace('🟢 ', '').replace('🟡 ', '').replace('🔴 ', ''),
                "enrichment_temperature": enriched_data.get('temperature'),
                "enrichment_weather_description": enriched_data.get('weather_description'),
                "enrichment_median_income": enriched_data.get('median_income'),
                "enrichment_percent_renters": enriched_data.get('percent_renters'),
                "enrichment_population": enriched_data.get('population'),
                "enrichment_insights": enriched_data.get('insights'),
                "enrichment_outreach_message": enriched_data.get('outreach_message'),
                "enrichment_enrichment_status": "Success"
            }
            return self.crm.update_hubspot_contact(record_id, properties)
        elif self.crm_type == 'salesforce':
            record_type = enriched_data.get('record_type', 'Lead')
            fields = {
                "Enrichment_Lead_Score__c": enriched_data.get('score'),
                "Enrichment_Score_Category__c": enriched_data.get('score_category', '').replace('🟢 ', '').replace('🟡 ', '').replace('🔴 ', ''),
                "Enrichment_Temperature__c": enriched_data.get('temperature'),
                "Enrichment_Weather_Description__c": enriched_data.get('weather_description'),
                "Enrichment_Median_Income__c": enriched_data.get('median_income'),
                "Enrichment_Percent_Renters__c": enriched_data.get('percent_renters'),
                "Enrichment_Population__c": enriched_data.get('population'),
                "Enrichment_Insights__c": enriched_data.get('insights'),
                "Enrichment_Outreach_Message__c": enriched_data.get('outreach_message'),
                "Enrichment_Enrichment_Status__c": "Success"
            }
            return self.crm.update_salesforce_record(record_id, record_type, fields)
    
    def bulk_sync(self, leads: List[Dict]) -> Dict:
        """
        Bulk sync multiple leads to CRM
        
        Args:
            leads: List of lead dictionaries
        
        Returns:
            dict: Summary of sync results
        """
        if self.crm_type == 'hubspot':
            return self.crm.bulk_sync_leads(leads)
        elif self.crm_type == 'salesforce':
            record_type = leads[0].get('record_type', 'Lead') if leads else 'Lead'
            return self.crm.bulk_sync_leads(leads, record_type)
    
    def search_by_email(self, email: str) -> Optional[Dict]:
        """
        Search for record by email address
        
        Args:
            email: Email address to search for
        
        Returns:
            dict: Record data if found, None otherwise
        """
        if self.crm_type == 'hubspot':
            return self.crm.search_contact_by_email(email)
        elif self.crm_type == 'salesforce':
            # Try Lead first, then Contact
            result = self.crm.search_by_email(email, "Lead")
            if result:
                return result
            return self.crm.search_by_email(email, "Contact")

def create_crm_sync(crm_type: str, **kwargs) -> UnifiedCRMSync:
    """
    Factory function to create CRM sync instance
    
    Args:
        crm_type: Type of CRM ('hubspot' or 'salesforce')
        **kwargs: Additional arguments for CRM initialization
    
    Returns:
        UnifiedCRMSync: CRM sync instance
    """
    return UnifiedCRMSync(crm_type, **kwargs)

