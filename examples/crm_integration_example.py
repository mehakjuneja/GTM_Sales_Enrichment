"""
Example: CRM Integration
Demonstrates how to sync leads between lead enrichment system and CRM systems
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_calls import enrich_lead_data
from utils.scoring import calculate_lead_score, categorize_score
from utils.enhanced_scoring import calculate_enhanced_lead_score
from utils.clay_integration import ClayIntegration
from utils.crm_sync import create_crm_sync

load_dotenv()

def example_hubspot_sync():
    """Example: Sync lead to HubSpot"""
    print("=" * 60)
    print("Example: HubSpot Integration")
    print("=" * 60)
    
    try:
        # Initialize HubSpot sync
        crm = create_crm_sync('hubspot')
        
        # Sample lead data
        lead_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'company': 'ABC Property Management',
            'city': 'San Francisco',
            'state': 'CA',
            'country': 'USA'
        }
        
        print(f"\n1. Enriching lead: {lead_data['name']} from {lead_data['company']}")
        
        # Enrich lead data
        enriched = enrich_lead_data(
            city=lead_data['city'],
            state=lead_data['state'],
            country=lead_data['country']
        )
        
        # Calculate score
        score = calculate_lead_score(
            enriched.get('percent_renters', 0),
            enriched.get('median_income', 0),
            enriched.get('temperature', 0)
        )
        
        print(f"   Score: {score}/100 ({categorize_score(score)})")
        
        # Prepare data for CRM
        lead_data.update({
            'score': score,
            'score_category': categorize_score(score),
            'temperature': enriched.get('temperature'),
            'weather_description': enriched.get('weather_description'),
            'median_income': enriched.get('median_income'),
            'percent_renters': enriched.get('percent_renters'),
            'population': enriched.get('population')
        })
        
        print(f"\n2. Syncing to HubSpot...")
        
        # Sync to HubSpot
        result = crm.sync_enriched_lead(lead_data)
        print(f"   ✅ Successfully synced! Contact ID: {result.get('id', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   Make sure HUBSPOT_API_KEY is set in .env file")

def example_salesforce_sync():
    """Example: Sync lead to Salesforce"""
    print("\n" + "=" * 60)
    print("Example: Salesforce Integration")
    print("=" * 60)
    
    try:
        # Initialize Salesforce sync
        crm = create_crm_sync('salesforce')
        
        # Sample lead data
        lead_data = {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'company': 'XYZ Real Estate',
            'city': 'Austin',
            'state': 'TX',
            'country': 'USA',
            'record_type': 'Lead'
        }
        
        print(f"\n1. Enriching lead: {lead_data['name']} from {lead_data['company']}")
        
        # Enrich lead data
        enriched = enrich_lead_data(
            city=lead_data['city'],
            state=lead_data['state'],
            country=lead_data['country']
        )
        
        # Calculate score
        score = calculate_lead_score(
            enriched.get('percent_renters', 0),
            enriched.get('median_income', 0),
            enriched.get('temperature', 0)
        )
        
        print(f"   Score: {score}/100 ({categorize_score(score)})")
        
        # Prepare data for CRM
        lead_data.update({
            'score': score,
            'score_category': categorize_score(score),
            'temperature': enriched.get('temperature'),
            'weather_description': enriched.get('weather_description'),
            'median_income': enriched.get('median_income'),
            'percent_renters': enriched.get('percent_renters'),
            'population': enriched.get('population')
        })
        
        print(f"\n2. Syncing to Salesforce...")
        
        # Sync to Salesforce
        result = crm.sync_enriched_lead(lead_data)
        print(f"   ✅ Successfully synced! Record ID: {result.get('id', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   Make sure Salesforce credentials are set in .env file")

def example_clay_enhancement():
    """Example: Enhanced scoring with Clay data"""
    print("\n" + "=" * 60)
    print("Example: Clay Enhancement")
    print("=" * 60)
    
    try:
        # Initialize Clay
        clay = ClayIntegration()
        
        # Sample lead
        lead_data = {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'company': 'Property Pro Management',
            'city': 'Seattle',
            'state': 'WA',
            'country': 'USA'
        }
        
        print(f"\n1. Enriching with Clay: {lead_data['company']}")
        
        # Enrich with Clay
        enhanced = clay.enrich_with_clay_insights(lead_data)
        
        if enhanced.get('clay_company_data'):
            print(f"   ✅ Company enriched!")
            print(f"   - Employee Count: {enhanced.get('clay_employee_count', 'N/A')}")
            print(f"   - Industry: {enhanced.get('clay_industry', 'N/A')}")
            print(f"   - Revenue: ${enhanced.get('clay_revenue', 0):,}" if enhanced.get('clay_revenue') else "   - Revenue: N/A")
        else:
            print(f"   ⚠️ Clay enrichment not available (check API key)")
        
        # Enrich with existing APIs
        enriched = enrich_lead_data(
            city=lead_data['city'],
            state=lead_data['state'],
            country=lead_data['country']
        )
        
        # Calculate enhanced score
        clay_data = {
            'employee_count': enhanced.get('clay_employee_count'),
            'revenue': enhanced.get('clay_revenue'),
            'industry': enhanced.get('clay_industry'),
            'total_funding': enhanced.get('clay_funding')
        }
        
        enhanced_score = calculate_enhanced_lead_score(
            enriched.get('percent_renters', 0),
            enriched.get('median_income', 0),
            enriched.get('temperature', 0),
            clay_company_data=clay_data if any(clay_data.values()) else None
        )
        
        base_score = calculate_lead_score(
            enriched.get('percent_renters', 0),
            enriched.get('median_income', 0),
            enriched.get('temperature', 0)
        )
        
        print(f"\n2. Scoring Results:")
        print(f"   Base Score: {base_score}/100")
        print(f"   Enhanced Score: {enhanced_score}/100")
        print(f"   Bonus: +{enhanced_score - base_score} points from Clay data")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   Make sure CLAY_API_KEY is set in .env file")

def example_full_workflow():
    """Example: Full workflow with CRM + Clay"""
    print("\n" + "=" * 60)
    print("Example: Full Workflow (CRM + Clay + Enhanced Scoring)")
    print("=" * 60)
    
    # This would be the complete workflow:
    # 1. Get leads from CRM
    # 2. Enrich with Clay
    # 3. Enrich with existing APIs
    # 4. Calculate enhanced score
    # 5. Update CRM with results
    
    print("\nFull workflow would include:")
    print("1. Fetch unenriched leads from CRM")
    print("2. Enrich with Clay (company/contact data)")
    print("3. Enrich with OpenWeather + DataUSA APIs")
    print("4. Calculate enhanced score (base + Clay + CRM bonuses)")
    print("5. Update CRM with enriched data and scores")
    print("6. Generate outreach messages")
    print("7. Log activities in CRM")
    
    print("\n💡 See CRM_INTEGRATION_GUIDE.md for complete implementation")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CRM Integration Examples")
    print("=" * 60)
    
    # Run examples (comment out the ones you don't have configured)
    # example_hubspot_sync()
    # example_salesforce_sync()
    # example_clay_enhancement()
    example_full_workflow()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set up your CRM credentials in .env file")
    print("2. Install required dependencies: pip install -r requirements.txt")
    print("3. Create custom fields in your CRM (see CRM_INTEGRATION_GUIDE.md)")
    print("4. Test with sample leads")
    print("5. Integrate into your workflow")

