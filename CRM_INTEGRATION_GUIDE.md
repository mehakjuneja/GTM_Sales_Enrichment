# CRM & Enrichment Integration Guide

## Overview
This guide outlines how to integrate the lead enrichment and scoring system with industry-standard CRMs (HubSpot, Salesforce) and enrichment platforms (Clay) to create a seamless workflow.

---

## 🎯 Integration Architecture

### Current State
- **Data Source**: Manual input via Streamlit form
- **Enrichment**: OpenWeather + DataUSA APIs
- **Storage**: CSV files
- **Scoring**: Custom algorithm (rental %, income, weather)
- **Outreach**: AI-generated messages

### Target State
- **Data Source**: CRM systems (HubSpot/Salesforce) + Clay enrichment
- **Enrichment**: Clay API + existing APIs
- **Storage**: CRM systems (single source of truth)
- **Scoring**: Enhanced with CRM data + Clay enrichment
- **Outreach**: Automated CRM updates + email campaigns

---

## 🔄 Integration Patterns

### Pattern 1: CRM → Enrichment System → CRM (Bidirectional Sync)
```
CRM Lead Created → Webhook → Enrichment → Score Calculation → 
Update CRM Record → Generate Outreach → Log Activity in CRM
```

### Pattern 2: Clay → Enrichment System → CRM (Enrichment Pipeline)
```
Clay Enrichment → Scoring → CRM Update → Outreach Automation
```

### Pattern 3: Enrichment System → CRM → Clay (Hybrid Workflow)
```
Manual Lead Entry → Enrichment → CRM Sync → 
Clay Additional Enrichment → Re-score → CRM Update
```

---

## 📊 HubSpot Integration

### 1. HubSpot API Setup

#### Required Credentials
```env
HUBSPOT_API_KEY=your_hubspot_api_key
HUBSPOT_PORTAL_ID=your_portal_id
HUBSPOT_APP_ID=your_app_id  # For OAuth apps
```

#### Custom Properties to Create in HubSpot
- `enrichment_lead_score` (Number) - 0-100 score
- `enrichment_score_category` (Single-select) - High/Medium/Low
- `enrichment_temperature` (Number) - Current temperature
- `enrichment_weather_description` (Text) - Weather description
- `enrichment_median_income` (Number) - Area median income
- `enrichment_percent_renters` (Number) - Rental market percentage
- `enrichment_population` (Number) - Area population
- `enrichment_insights` (Text) - Market insights
- `enrichment_outreach_message` (Text) - Generated outreach message
- `enrichment_enriched_at` (Date) - Last enrichment timestamp
- `enrichment_enrichment_status` (Single-select) - Success/Failed/Pending

### 2. HubSpot Integration Features

#### A. Lead Sync (HubSpot → Enrichment System)
- **Webhook Listener**: Listen for new contact/company creation
- **Auto-Enrichment**: Trigger enrichment when lead is created
- **Bulk Import**: Sync existing HubSpot leads

#### B. Data Push (Enrichment System → HubSpot)
- **Score Updates**: Push calculated scores to HubSpot properties
- **Activity Logging**: Log enrichment activities as notes/timeline events
- **Deal Association**: Link enriched leads to deals
- **Workflow Triggers**: Trigger HubSpot workflows based on scores

#### C. Two-Way Sync
- **Real-time Updates**: Sync changes bidirectionally
- **Conflict Resolution**: Handle data conflicts intelligently
- **Sync Status**: Track sync status and errors

### 3. Implementation Code Structure

```python
# utils/hubspot_integration.py
class HubSpotIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
    
    def create_custom_properties(self):
        """Create custom properties in HubSpot"""
        pass
    
    def sync_lead_to_hubspot(self, lead_data):
        """Push enriched lead data to HubSpot"""
        pass
    
    def get_hubspot_leads(self, filters=None):
        """Pull leads from HubSpot for enrichment"""
        pass
    
    def update_hubspot_contact(self, contact_id, properties):
        """Update HubSpot contact with enrichment data"""
        pass
    
    def log_activity(self, contact_id, activity_data):
        """Log enrichment activity in HubSpot timeline"""
        pass
```

---

## 💼 Salesforce Integration

### 1. Salesforce API Setup

#### Required Credentials
```env
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_security_token
SALESFORCE_CONSUMER_KEY=your_consumer_key
SALESFORCE_CONSUMER_SECRET=your_consumer_secret
SALESFORCE_INSTANCE_URL=https://yourinstance.salesforce.com
```

#### Custom Fields to Create in Salesforce
- `Enrichment_Lead_Score__c` (Number) - 0-100 score
- `Enrichment_Score_Category__c` (Picklist) - High/Medium/Low
- `Enrichment_Temperature__c` (Number) - Current temperature
- `Enrichment_Weather_Description__c` (Text) - Weather description
- `Enrichment_Median_Income__c` (Currency) - Area median income
- `Enrichment_Percent_Renters__c` (Percent) - Rental market percentage
- `Enrichment_Population__c` (Number) - Area population
- `Enrichment_Insights__c` (Long Text Area) - Market insights
- `Enrichment_Outreach_Message__c` (Long Text Area) - Generated message
- `Enrichment_Enriched_At__c` (DateTime) - Last enrichment timestamp
- `Enrichment_Enrichment_Status__c` (Picklist) - Success/Failed/Pending

### 2. Salesforce Integration Features

#### A. Lead/Contact Sync
- **SOQL Queries**: Query leads/contacts for enrichment
- **Bulk API**: Handle large volumes efficiently
- **Change Data Capture**: Listen for real-time changes

#### B. Data Updates
- **Field Updates**: Update custom fields with enrichment data
- **Task Creation**: Create follow-up tasks based on scores
- **Email Template Integration**: Use Salesforce email templates
- **Campaign Association**: Link to marketing campaigns

#### C. Automation
- **Process Builder**: Trigger workflows based on scores
- **Flow Automation**: Automated enrichment workflows
- **Apex Triggers**: Custom business logic

### 3. Implementation Code Structure

```python
# utils/salesforce_integration.py
from simple_salesforce import Salesforce

class SalesforceIntegration:
    def __init__(self, username, password, security_token, 
                 consumer_key, consumer_secret):
        self.sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )
    
    def create_custom_fields(self):
        """Create custom fields via Metadata API"""
        pass
    
    def sync_lead_to_salesforce(self, lead_data):
        """Push enriched lead data to Salesforce"""
        pass
    
    def get_salesforce_leads(self, filters=None):
        """Pull leads from Salesforce for enrichment"""
        pass
    
    def update_salesforce_record(self, record_id, record_type, fields):
        """Update Salesforce record with enrichment data"""
        pass
    
    def create_task(self, record_id, task_data):
        """Create follow-up task in Salesforce"""
        pass
```

---

## 🎨 Clay Integration

### 1. Clay API Setup

#### Required Credentials
```env
CLAY_API_KEY=your_clay_api_key
CLAY_WORKSPACE_ID=your_workspace_id
```

#### Clay Enrichment Data Points
Clay can provide additional enrichment beyond current APIs:
- **Company Data**: Industry, employee count, revenue, funding
- **Contact Data**: Job title, LinkedIn profile, social profiles
- **Technographic Data**: Tech stack, software usage
- **Intent Data**: Buying signals, content engagement
- **Firmographic Data**: Company size, growth rate, location details

### 2. Clay Integration Features

#### A. Enrichment Pipeline
- **Pre-Enrichment**: Use Clay to get company/contact data before scoring
- **Post-Enrichment**: Enhance existing enriched data with Clay insights
- **Bulk Enrichment**: Process multiple leads through Clay

#### B. Data Enhancement
- **Company Intelligence**: Add company-level insights to scoring
- **Contact Intelligence**: Personalize outreach with contact data
- **Technographic Scoring**: Factor tech stack into lead scoring

#### C. Workflow Integration
- **Clay Tables**: Sync with Clay tables for enrichment workflows
- **Clay Actions**: Trigger Clay actions based on scores
- **Clay Webhooks**: Receive Clay enrichment results

### 3. Implementation Code Structure

```python
# utils/clay_integration.py
import requests

class ClayIntegration:
    def __init__(self, api_key, workspace_id):
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.base_url = "https://api.clay.com/v1"
    
    def enrich_company(self, company_name, domain=None):
        """Enrich company data via Clay"""
        pass
    
    def enrich_contact(self, email, name=None):
        """Enrich contact data via Clay"""
        pass
    
    def bulk_enrich(self, leads):
        """Bulk enrich multiple leads"""
        pass
    
    def get_clay_table_data(self, table_name):
        """Retrieve data from Clay table"""
        pass
    
    def update_clay_table(self, table_name, data):
        """Update Clay table with enrichment results"""
        pass
```

---

## 🔧 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
1. **Create Integration Modules**
   - `utils/hubspot_integration.py`
   - `utils/salesforce_integration.py`
   - `utils/clay_integration.py`
   - `utils/crm_sync.py` (unified interface)

2. **Environment Setup**
   - Add CRM credentials to `.env`
   - Create custom properties/fields in CRMs
   - Set up API connections

3. **Basic Sync Functionality**
   - Pull leads from CRM
   - Push enrichment data back
   - Error handling and logging

### Phase 2: Enhanced Scoring (Week 3-4)
1. **Integrate Clay Data**
   - Add Clay enrichment to pipeline
   - Enhance scoring with Clay insights
   - Update scoring algorithm

2. **CRM-Specific Scoring**
   - Factor in CRM activity data
   - Use CRM engagement scores
   - Combine with enrichment scores

3. **Automated Workflows**
   - Auto-enrich on lead creation
   - Trigger workflows based on scores
   - Automated outreach scheduling

### Phase 3: Advanced Features (Week 5-6)
1. **Bidirectional Sync**
   - Real-time updates
   - Conflict resolution
   - Sync status tracking

2. **Advanced Analytics**
   - Score trends over time
   - Conversion tracking
   - ROI measurement

3. **Workflow Automation**
   - Automated enrichment schedules
   - Smart routing based on scores
   - Integration with email campaigns

---

## 📝 Code Examples

### Example 1: HubSpot Lead Sync

```python
from utils.hubspot_integration import HubSpotIntegration
from utils.api_calls import enrich_lead_data
from utils.scoring import calculate_lead_score

# Initialize HubSpot
hubspot = HubSpotIntegration(api_key=os.getenv('HUBSPOT_API_KEY'))

# Get new leads from HubSpot
new_leads = hubspot.get_hubspot_leads(
    filters={'property': 'enrichment_enriched_at', 'operator': 'NOT_HAS_PROPERTY'}
)

# Enrich and score each lead
for lead in new_leads:
    # Enrich with existing APIs
    enriched = enrich_lead_data(
        city=lead['properties']['city'],
        state=lead['properties']['state'],
        country=lead['properties']['country']
    )
    
    # Calculate score
    score = calculate_lead_score(
        enriched['percent_renters'],
        enriched['median_income'],
        enriched['temperature']
    )
    
    # Update HubSpot
    hubspot.update_hubspot_contact(lead['id'], {
        'enrichment_lead_score': score,
        'enrichment_temperature': enriched['temperature'],
        'enrichment_median_income': enriched['median_income'],
        'enrichment_percent_renters': enriched['percent_renters'],
        'enrichment_enriched_at': datetime.now().isoformat()
    })
```

### Example 2: Clay + Salesforce Integration

```python
from utils.clay_integration import ClayIntegration
from utils.salesforce_integration import SalesforceIntegration
from utils.scoring import calculate_enhanced_lead_score

# Initialize integrations
clay = ClayIntegration(api_key=os.getenv('CLAY_API_KEY'))
salesforce = SalesforceIntegration(...)

# Get leads from Salesforce
leads = salesforce.get_salesforce_leads(
    filters={'Enrichment_Enriched_At__c': None}
)

# Enrich with Clay
for lead in leads:
    # Clay enrichment
    clay_data = clay.enrich_company(
        company_name=lead['Company'],
        domain=lead.get('Website')
    )
    
    # Existing enrichment
    enriched = enrich_lead_data(
        city=lead['City'],
        state=lead['State'],
        country=lead['Country']
    )
    
    # Enhanced scoring with Clay data
    score = calculate_enhanced_lead_score(
        enriched, clay_data
    )
    
    # Update Salesforce
    salesforce.update_salesforce_record(
        record_id=lead['Id'],
        record_type='Lead',
        fields={
            'Enrichment_Lead_Score__c': score,
            'Enrichment_Company_Size__c': clay_data.get('employee_count'),
            'Enrichment_Industry__c': clay_data.get('industry')
        }
    )
```

### Example 3: Webhook Handler for Real-time Sync

```python
from flask import Flask, request, jsonify
from utils.crm_sync import sync_lead_to_all_crms

app = Flask(__name__)

@app.route('/webhook/hubspot', methods=['POST'])
def hubspot_webhook():
    """Handle HubSpot webhook for new lead creation"""
    data = request.json
    
    if data['subscriptionType'] == 'contact.creation':
        contact = data['properties']
        
        # Enrich lead
        enriched = enrich_lead_data(
            city=contact.get('city'),
            state=contact.get('state'),
            country=contact.get('country')
        )
        
        # Calculate score
        score = calculate_lead_score(...)
        
        # Update HubSpot
        hubspot.update_hubspot_contact(
            contact_id=data['objectId'],
            properties={'enrichment_lead_score': score, ...}
        )
        
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'ignored'})
```

---

## 🎯 Best Practices

### 1. Data Mapping
- **Standardize Fields**: Create mapping between CRM fields and enrichment data
- **Handle Missing Data**: Gracefully handle missing or incomplete data
- **Data Validation**: Validate data before syncing

### 2. Error Handling
- **Retry Logic**: Implement retry for failed API calls
- **Error Logging**: Log all errors for debugging
- **Fallback Mechanisms**: Fall back to manual processes when APIs fail

### 3. Rate Limiting
- **Respect API Limits**: Implement rate limiting for all APIs
- **Batch Processing**: Process leads in batches to avoid limits
- **Queue System**: Use queues for async processing

### 4. Security
- **API Key Management**: Store credentials securely
- **OAuth Where Possible**: Use OAuth for better security
- **Data Encryption**: Encrypt sensitive data in transit and at rest

### 5. Monitoring
- **Sync Status Dashboard**: Track sync status and errors
- **Performance Metrics**: Monitor API response times
- **Alerting**: Set up alerts for critical failures

---

## 📊 Enhanced Scoring with CRM Data

### Additional Scoring Factors

1. **CRM Engagement Score**
   - Email opens/clicks
   - Website visits
   - Content engagement
   - Meeting attendance

2. **Clay Enrichment Data**
   - Company size (employee count)
   - Revenue range
   - Funding stage
   - Tech stack alignment
   - Industry fit

3. **Historical Data**
   - Previous interactions
   - Deal history
   - Conversion probability
   - Time in CRM

### Updated Scoring Algorithm

```python
def calculate_enhanced_lead_score(
    percent_renters, median_income, temperature,
    crm_engagement_score=None,
    clay_company_data=None,
    historical_data=None
):
    # Base score (existing algorithm)
    base_score = calculate_lead_score(
        percent_renters, median_income, temperature
    )
    
    # CRM engagement bonus (0-10 points)
    crm_bonus = 0
    if crm_engagement_score:
        crm_bonus = min(10, crm_engagement_score / 10)
    
    # Clay company data bonus (0-10 points)
    clay_bonus = 0
    if clay_company_data:
        # Factor in company size, revenue, etc.
        if clay_company_data.get('employee_count', 0) > 50:
            clay_bonus += 5
        if clay_company_data.get('revenue', 0) > 1000000:
            clay_bonus += 5
    
    # Historical data bonus (0-10 points)
    history_bonus = 0
    if historical_data:
        if historical_data.get('has_previous_interaction'):
            history_bonus += 5
        if historical_data.get('conversion_probability', 0) > 0.5:
            history_bonus += 5
    
    total_score = base_score + crm_bonus + clay_bonus + history_bonus
    return min(100, total_score)
```

---

## 🚀 Quick Start Integration

### Step 1: Install Dependencies
```bash
pip install hubspot-api-client simple-salesforce requests python-dotenv
```

### Step 2: Add Environment Variables
```env
# HubSpot
HUBSPOT_API_KEY=your_key

# Salesforce
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token

# Clay
CLAY_API_KEY=your_key
CLAY_WORKSPACE_ID=your_workspace
```

### Step 3: Create Integration Module
Create `utils/crm_integration.py` with basic sync functions

### Step 4: Update App
Add CRM sync buttons and configuration to Streamlit app

### Step 5: Test Integration
Test with sample leads before full deployment

---

## 📈 Expected Benefits

1. **Single Source of Truth**: All data in CRM, no CSV files
2. **Automated Workflows**: Enrichment happens automatically
3. **Better Scoring**: Enhanced with CRM and Clay data
4. **Improved Outreach**: More personalized with enriched data
5. **Scalability**: Handle thousands of leads efficiently
6. **Analytics**: Track ROI and conversion rates
7. **Team Collaboration**: Sales team works in familiar CRM

---

## 🔍 Next Steps

1. **Choose Primary CRM**: Decide on HubSpot vs Salesforce
2. **Set Up Credentials**: Get API keys and configure access
3. **Create Custom Fields**: Set up properties/fields in CRM
4. **Build Integration Module**: Start with basic sync functionality
5. **Test with Sample Data**: Validate integration before production
6. **Deploy Gradually**: Roll out to team incrementally
7. **Monitor and Optimize**: Track performance and improve

---

## 📚 Additional Resources

- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [Salesforce REST API Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Clay API Documentation](https://docs.clay.com/)
- [Webhook Best Practices](https://webhooks.fyi/)

---

## ❓ FAQ

**Q: Can I use both HubSpot and Salesforce?**
A: Yes, but you'll need to choose one as primary or implement a unified sync layer.

**Q: How often should I sync data?**
A: Real-time for new leads, hourly/daily for bulk updates depending on volume.

**Q: What if Clay enrichment fails?**
A: Fall back to existing enrichment APIs and log the error.

**Q: How do I handle data conflicts?**
A: Implement a conflict resolution strategy (e.g., CRM data takes precedence, or timestamp-based).

**Q: Can I enrich existing leads?**
A: Yes, implement a bulk enrichment feature that processes existing CRM records.

