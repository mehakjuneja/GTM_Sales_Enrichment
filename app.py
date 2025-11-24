import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.api_calls import enrich_lead_data
from utils.scoring import calculate_lead_score, categorize_score
from utils.outreach import generate_outreach_message, generate_llm_outreach_message
from utils.email_sender import EmailSender, test_email_configuration, send_test_email
from utils.mail_app_sender import MailAppSender
from utils.gmail_web_sender import GmailWebSender

# CSV file path for persistent storage
CSV_FILE_PATH = "/Users/mehakjuneja/Documents/EliseAI/data/leads.csv"

# Page configuration
st.set_page_config(
    page_title="Lead Enrichment & Outreach Assistant",
    page_icon="🏠",
    layout="wide"
)

def load_leads_from_csv():
    """Load leads from CSV file"""
    try:
        if os.path.exists(CSV_FILE_PATH):
            df = pd.read_csv(CSV_FILE_PATH)
            # Convert timestamp column back to datetime
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        else:
            return pd.DataFrame(columns=[
                'timestamp', 'name', 'email', 'company', 'property_address', 
                'city', 'state', 'country', 'temperature', 'weather_description',
                'median_income', 'population', 'percent_renters', 'score', 
                'score_category', 'insights', 'outreach_message'
            ])
    except Exception as e:
        st.error(f"Error loading leads from CSV: {e}")
        return pd.DataFrame(columns=[
            'timestamp', 'name', 'email', 'company', 'property_address', 
            'city', 'state', 'country', 'temperature', 'weather_description',
            'median_income', 'population', 'percent_renters', 'score', 
            'score_category', 'insights', 'outreach_message'
        ])

def save_leads_to_csv(df):
    """Save leads to CSV file"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
        df.to_csv(CSV_FILE_PATH, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving leads to CSV: {e}")
        return False

# Initialize session state for leads storage
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = load_leads_from_csv()

# Initialize LLM settings
if 'use_llm' not in st.session_state:
    st.session_state.use_llm = True

def main():
    st.title("🏠 Lead Enrichment & Outreach Assistant")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Add New Lead", "Lead Dashboard", "Settings"])
    
    if page == "Add New Lead":
        show_lead_form()
    elif page == "Lead Dashboard":
        show_dashboard()
    elif page == "Settings":
        show_settings()

def show_lead_form():
    st.header("📝 Add New Lead")
    st.markdown("Enter lead information to trigger enrichment and outreach generation.")
    
    with st.form("lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="John Doe")
            email = st.text_input("Email *", placeholder="john@company.com")
            company = st.text_input("Company *", placeholder="ABC Property Management")
            property_address = st.text_input("Property Address", placeholder="123 Main St")
        
        with col2:
            city = st.text_input("City *", placeholder="San Francisco")
            state = st.text_input("State *", placeholder="CA")
            country = st.text_input("Country *", placeholder="USA")
        
        submitted = st.form_submit_button("🚀 Enrich Lead & Generate Outreach", type="primary")
        
        if submitted:
            # Validate required fields
            required_fields = [name, email, company, city, state, country]
            if not all(required_fields):
                st.error("Please fill in all required fields (marked with *)")
                return
            
            # Show loading spinner
            with st.spinner("Enriching lead data and generating outreach..."):
                try:
                    # Enrich lead data
                    enriched_data = enrich_lead_data(city, state, country)
                    
                    # Calculate lead score
                    score = calculate_lead_score(
                        enriched_data.get('percent_renters', 0),
                        enriched_data.get('median_income', 0),
                        enriched_data.get('temperature', 0)
                    )
                    score_category = categorize_score(score)
                    
                    # Generate insights
                    insights = generate_insights(enriched_data)
                    
                    # Generate outreach message
                    if st.session_state.use_llm:
                        try:
                            outreach_message = generate_llm_outreach_message(
                                name, company, city, state, 
                                enriched_data.get('weather_description', 'pleasant'),
                                enriched_data.get('temperature', 70),
                                enriched_data.get('median_income', 55000),
                                enriched_data.get('percent_renters', 40),
                                enriched_data.get('population', 100000),
                                insights
                            )
                            st.info("🤖 Generated using AI for maximum personalization")
                        except Exception as e:
                            st.warning(f"⚠️ AI generation failed, using template: {str(e)}")
                            outreach_message = generate_outreach_message(
                                name, company, city, enriched_data.get('weather_description', 'pleasant'),
                                insights
                            )
                    else:
                        outreach_message = generate_outreach_message(
                            name, company, city, enriched_data.get('weather_description', 'pleasant'),
                            insights
                        )
                        st.info("📝 Generated using template-based approach")
                    
                    # Create new lead record
                    new_lead = {
                        'timestamp': datetime.now(),
                        'name': name,
                        'email': email,
                        'company': company,
                        'property_address': property_address,
                        'city': city,
                        'state': state,
                        'country': country,
                        'temperature': enriched_data.get('temperature', 0),
                        'weather_description': enriched_data.get('weather_description', 'N/A'),
                        'median_income': enriched_data.get('median_income', 0),
                        'population': enriched_data.get('population', 0),
                        'percent_renters': enriched_data.get('percent_renters', 0),
                        'score': score,
                        'score_category': score_category,
                        'insights': insights,
                        'outreach_message': outreach_message
                    }
                    
                    # Add to session state
                    new_row_df = pd.DataFrame([new_lead])
                    st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_row_df], ignore_index=True)
                    
                    # Save to CSV file for persistence
                    if save_leads_to_csv(st.session_state.leads_df):
                        st.success("✅ Lead enriched, outreach generated, and saved successfully!")
                    else:
                        st.success("✅ Lead enriched and outreach generated successfully!")
                        st.warning("⚠️ Lead saved in session but couldn't save to file")
                    
                    # Display results
                    st.subheader("📊 Enrichment Results")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Lead Score", f"{score}/100", score_category)
                        st.metric("Temperature", f"{enriched_data.get('temperature', 0)}°F")
                    
                    with col2:
                        st.metric("Median Income", f"${enriched_data.get('median_income', 0):,}")
                        st.metric("Population", f"{enriched_data.get('population', 0):,}")
                    
                    with col3:
                        st.metric("% Renters", f"{enriched_data.get('percent_renters', 0):.1f}%")
                        st.metric("Weather", enriched_data.get('weather_description', 'N/A'))
                    
                    st.subheader("💬 Generated Outreach Message")
                    st.text_area("Copy this message:", outreach_message, height=200)
                    
                except Exception as e:
                    st.error(f"Error enriching lead: {str(e)}")
                    st.info("Please check your API keys in Settings and try again.")

def show_dashboard():
    st.header("📊 Lead Dashboard")
    
    # Show save status and refresh option
    total_leads = len(st.session_state.leads_df)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if total_leads > 0:
            st.success(f"💾 {total_leads} leads saved and loaded from storage")
        else:
            st.info("No leads found. Add a new lead to see the dashboard.")
    
    with col2:
        if st.button("🔄 Refresh Data"):
            st.session_state.leads_df = load_leads_from_csv()
            st.rerun()
    
    if total_leads == 0:
        return
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_filter = st.selectbox("Score Category", ["All", "High", "Medium", "Low"])
    with col2:
        city_filter = st.selectbox("City", ["All"] + list(st.session_state.leads_df['city'].unique()))
    with col3:
        export_format = st.selectbox("Export Format", ["CSV", "Excel"])
    
    # Apply filters
    filtered_df = st.session_state.leads_df.copy()
    
    if score_filter != "All":
        filtered_df = filtered_df[filtered_df['score_category'] == score_filter]
    
    if city_filter != "All":
        filtered_df = filtered_df[filtered_df['city'] == city_filter]
    
    # Display metrics
    st.subheader("📈 Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", len(filtered_df))
    with col2:
        avg_score = filtered_df['score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}")
    with col3:
        high_score_leads = len(filtered_df[filtered_df['score_category'] == 'High'])
        st.metric("High Score Leads", high_score_leads)
    with col4:
        st.metric("Cities Covered", filtered_df['city'].nunique())
    
    # Display leads table
    st.subheader("📋 Leads Table")
    
    # Prepare display dataframe
    display_df = filtered_df.copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    display_df = display_df.rename(columns={
        'timestamp': 'Date Added',
        'name': 'Name',
        'email': 'Email',
        'company': 'Company',
        'city': 'City',
        'score': 'Score',
        'score_category': 'Category',
        'weather_description': 'Weather',
        'outreach_message': 'Outreach Message'
    })
    
    # Select columns to display
    display_columns = ['Date Added', 'Name', 'Email', 'Company', 'City', 'Score', 'Category', 'Weather']
    st.dataframe(display_df[display_columns], use_container_width=True)
    
    # Individual lead email functionality
    st.subheader("📧 Send Individual Emails")
    
    # Email method selection for individual emails
    individual_email_method = st.radio(
        "Choose email method for individual leads:",
        ["🌐 Gmail Web (Recommended)", "📱 Mac Mail App", "📧 SMTP Email (Requires Setup)"],
        key="individual_email_method",
        help="Select how you want to send emails to individual leads"
    )
    
    # Create a form for individual lead selection
    with st.form("individual_email_form"):
        st.write("**Select a lead to send an email to:**")
        
        # Create a selectbox with lead names and details
        lead_options = []
        for idx, row in filtered_df.iterrows():
            lead_option = f"{row['name']} ({row['company']}) - {row['email']} - Score: {row['score']}"
            lead_options.append((idx, lead_option))
        
        if lead_options:
            selected_lead_idx = st.selectbox(
                "Choose a lead:",
                options=[option[0] for option in lead_options],
                format_func=lambda x: next(option[1] for option in lead_options if option[0] == x),
                key="selected_lead"
            )
            
            # Get the selected lead data
            selected_lead = filtered_df.iloc[selected_lead_idx]
            
            # Show lead details
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Name:** {selected_lead['name']}")
                st.write(f"**Email:** {selected_lead['email']}")
            with col2:
                st.write(f"**Company:** {selected_lead['company']}")
                st.write(f"**City:** {selected_lead['city']}")
            with col3:
                st.write(f"**Score:** {selected_lead['score']} ({selected_lead['score_category']})")
            
            # Show outreach message preview
            st.write("**Outreach Message:**")
            st.text_area("", value=selected_lead['outreach_message'], height=100, disabled=True)
            
            # Submit button
            submitted = st.form_submit_button("📧 Send Email to This Lead", type="primary")
            
            if submitted:
                if individual_email_method == "🌐 Gmail Web (Recommended)":
                    with st.spinner("Opening Gmail for this lead..."):
                        gmail_sender = GmailWebSender()
                        success, message = gmail_sender.open_gmail_compose(
                            selected_lead.to_dict(), 
                            selected_lead['outreach_message']
                        )
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
                
                elif individual_email_method == "📱 Mac Mail App":
                    with st.spinner("Opening Mail app for this lead..."):
                        mail_sender = MailAppSender()
                        success, message = mail_sender.open_mail_app(
                            selected_lead.to_dict(), 
                            selected_lead['outreach_message']
                        )
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
                
                elif individual_email_method == "📧 SMTP Email (Requires Setup)":
                    with st.spinner("Sending email via SMTP..."):
                        email_sender = EmailSender()
                        if email_sender.is_configured():
                            success, message = email_sender.send_lead_email(
                                selected_lead.to_dict(), 
                                selected_lead['outreach_message']
                            )
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.error("❌ SMTP email not configured. Please set up email settings in the Settings page.")
        else:
            st.info("No leads available to send emails to.")
    
    # Bulk email functionality section
    st.subheader("📧 Bulk Email Campaigns")
    
    # Check for leads to email
    emailable_leads = filtered_df[filtered_df['email'].notna() & (filtered_df['email'] != '')]
    
    if len(emailable_leads) > 0:
        st.info(f"📬 Found {len(emailable_leads)} leads with email addresses ready for bulk campaigns")
        
        # Bulk email method selection
        bulk_email_method = st.radio(
            "Choose bulk email method:",
            ["🌐 Gmail Web (Recommended)", "📱 Mac Mail App", "📧 SMTP Email (Requires Setup)"],
            key="bulk_email_method",
            help="Select how you want to send bulk emails to multiple leads"
        )
        
        # Bulk email controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚀 Send Bulk Emails to All Leads", type="primary"):
                with st.spinner("Opening bulk email campaign..."):
                    if bulk_email_method == "🌐 Gmail Web (Recommended)":
                        gmail_sender = GmailWebSender()
                        success, result = gmail_sender.open_bulk_gmail_emails(emailable_leads, min_score=0)
                        
                        if success:
                            st.success(f"✅ {result['summary']}")
                            
                            # Show detailed results
                            with st.expander("📊 Bulk Email Results"):
                                for email_result in result['results']:
                                    status_icon = "✅" if email_result['success'] else "❌"
                                    st.write(f"{status_icon} {email_result['name']} ({email_result['company']}) - {email_result['message']}")
                        else:
                            st.error(f"❌ {result}")
                    
                    elif bulk_email_method == "📱 Mac Mail App":
                        mail_sender = MailAppSender()
                        success, result = mail_sender.open_bulk_emails(emailable_leads, min_score=0)
                        
                        if success:
                            st.success(f"✅ {result['summary']}")
                            
                            # Show detailed results
                            with st.expander("📊 Bulk Email Results"):
                                for email_result in result['results']:
                                    status_icon = "✅" if email_result['success'] else "❌"
                                    st.write(f"{status_icon} {email_result['name']} ({email_result['company']}) - {email_result['message']}")
                        else:
                            st.error(f"❌ {result}")
                    
                    elif bulk_email_method == "📧 SMTP Email (Requires Setup)":
                        email_sender = EmailSender()
                        if email_sender.is_configured():
                            success_count = 0
                            error_count = 0
                            
                            for idx, lead in emailable_leads.iterrows():
                                success, message = email_sender.send_lead_email(
                                    lead.to_dict(), 
                                    lead['outreach_message']
                                )
                                if success:
                                    success_count += 1
                                else:
                                    error_count += 1
                            
                            if success_count > 0:
                                st.success(f"✅ Successfully sent {success_count} emails!")
                            if error_count > 0:
                                st.error(f"❌ Failed to send {error_count} emails")
                        else:
                            st.error("❌ SMTP email not configured. Please set up email settings in the Settings page.")
        
        with col2:
            if st.button("🎯 Send to High-Priority Only"):
                high_priority_leads = emailable_leads[emailable_leads['score'] >= 71]
                
                if len(high_priority_leads) > 0:
                    with st.spinner(f"Opening emails for {len(high_priority_leads)} high-priority leads..."):
                        if bulk_email_method == "🌐 Gmail Web (Recommended)":
                            gmail_sender = GmailWebSender()
                            success, result = gmail_sender.open_bulk_gmail_emails(high_priority_leads, min_score=71)
                            
                            if success:
                                st.success(f"✅ {result['summary']}")
                            else:
                                st.error(f"❌ {result}")
                        
                        elif bulk_email_method == "📱 Mac Mail App":
                            mail_sender = MailAppSender()
                            success, result = mail_sender.open_bulk_emails(high_priority_leads, min_score=71)
                            
                            if success:
                                st.success(f"✅ {result['summary']}")
                            else:
                                st.error(f"❌ {result}")
                        
                        elif bulk_email_method == "📧 SMTP Email (Requires Setup)":
                            email_sender = EmailSender()
                            if email_sender.is_configured():
                                success_count = 0
                                for idx, lead in high_priority_leads.iterrows():
                                    success, message = email_sender.send_lead_email(
                                        lead.to_dict(), 
                                        lead['outreach_message']
                                    )
                                    if success:
                                        success_count += 1
                                
                                st.success(f"✅ Successfully sent {success_count} high-priority emails!")
                            else:
                                st.error("❌ SMTP email not configured. Please set up email settings in the Settings page.")
                else:
                    st.warning("No high-priority leads found (score ≥ 71)")
        
        with col3:
            if st.button("📊 Preview Bulk Campaign"):
                if len(emailable_leads) > 0:
                    sample_lead = emailable_leads.iloc[0]
                    sample_message = sample_lead.get('outreach_message', 'Sample outreach message')
                    
                    if bulk_email_method == "🌐 Gmail Web (Recommended)":
                        gmail_sender = GmailWebSender()
                        preview = gmail_sender.preview_email(sample_lead.to_dict(), sample_message)
                        
                        with st.expander("📧 Bulk Email Preview"):
                            st.markdown("**Sample Email Preview:**")
                            st.markdown(f"**To:** {preview['to']}")
                            st.markdown(f"**Subject:** {preview['subject']}")
                            st.markdown("**Content:**")
                            st.markdown(preview['body'].replace('\n', '\n\n'))
                    
                    elif bulk_email_method == "📱 Mac Mail App":
                        mail_sender = MailAppSender()
                        preview = mail_sender.preview_email(sample_lead.to_dict(), sample_message)
                        
                        with st.expander("📧 Bulk Email Preview"):
                            st.markdown("**Sample Email Preview:**")
                            st.markdown(f"**To:** {preview['to']}")
                            st.markdown(f"**Subject:** {preview['subject']}")
                            st.markdown("**Content:**")
                            st.markdown(preview['body'].replace('\n', '\n\n'))
                    
                    elif bulk_email_method == "📧 SMTP Email (Requires Setup)":
                        email_sender = EmailSender()
                        if email_sender.is_configured():
                            preview = email_sender.preview_email(sample_lead.to_dict(), sample_message)
                            
                            with st.expander("📧 Bulk Email Preview"):
                                st.markdown("**Sample Email Preview:**")
                                st.markdown(f"**To:** {preview['to']}")
                                st.markdown(f"**Subject:** {preview['subject']}")
                                st.markdown("**Content:**")
                                st.markdown(preview['body'].replace('\n', '\n\n'))
                        else:
                            st.error("❌ SMTP email not configured. Please set up email settings in the Settings page.")
        
        with col4:
            if st.button("📈 Campaign Statistics"):
                with st.expander("📊 Email Campaign Stats"):
                    st.metric("Total Leads", len(emailable_leads))
                    st.metric("High-Priority Leads", len(emailable_leads[emailable_leads['score'] >= 71]))
                    st.metric("Medium-Priority Leads", len(emailable_leads[(emailable_leads['score'] >= 51) & (emailable_leads['score'] <= 70)]))
                    st.metric("Low-Priority Leads", len(emailable_leads[emailable_leads['score'] <= 50]))
                    
                    # Show score distribution
                    st.write("**Score Distribution:**")
                    score_counts = emailable_leads['score_category'].value_counts()
                    for category, count in score_counts.items():
                        st.write(f"- {category}: {count} leads")
    else:
        st.warning("No leads with email addresses found. Please add leads with email addresses to use bulk email campaigns.")
    
    # Outreach messages section
    st.subheader("💬 Outreach Messages")
    for idx, row in filtered_df.iterrows():
        with st.expander(f"Message for {row['name']} ({row['company']})"):
            st.text(row['outreach_message'])
    
    # Export functionality
    st.subheader("📥 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download Filtered Data"):
            if export_format == "CSV":
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                # Excel export
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, sheet_name='Leads', index=False)
                st.download_button(
                    label="Download Excel",
                    data=output.getvalue(),
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col2:
        if st.button("Clear All Data", type="secondary"):
            if st.session_state.leads_df.empty:
                st.warning("No data to clear.")
            else:
                st.session_state.leads_df = pd.DataFrame(columns=st.session_state.leads_df.columns)
                # Also clear the CSV file
                save_leads_to_csv(st.session_state.leads_df)
                st.success("All data cleared!")
                st.rerun()
    
    # Email functionality section
    st.subheader("📧 Email High-Priority Leads")
    
    # Check for high-priority leads
    high_priority_leads = filtered_df[filtered_df['score'] >= 71]
    
    if len(high_priority_leads) > 0:
        st.info(f"🎯 Found {len(high_priority_leads)} high-priority leads (score ≥ 71) ready for email outreach")
        
        # Email method selection
        email_method = st.radio(
            "Choose email method:",
            ["🌐 Gmail Web (Recommended)", "📱 Mac Mail App", "📧 SMTP Email (Requires Setup)"],
            help="Gmail Web opens Gmail in your browser with pre-composed emails. Mac Mail App opens your default email client. SMTP sends emails directly."
        )
        
        if email_method == "🌐 Gmail Web (Recommended)":
            st.success("✅ Gmail Web - No password required!")
            st.info("This will open Gmail in your web browser with pre-composed emails for each lead.")
            
            # Gmail Web controls
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🌐 Open Gmail for All High-Priority Leads", type="primary"):
                    with st.spinner("Opening Gmail for high-priority leads..."):
                        gmail_sender = GmailWebSender()
                        success, result = gmail_sender.open_bulk_gmail_emails(high_priority_leads, min_score=71)
                        
                        if success:
                            st.success(f"✅ {result['summary']}")
                            
                            # Show detailed results
                            with st.expander("📊 Gmail Results Details"):
                                for email_result in result['results']:
                                    status_icon = "✅" if email_result['success'] else "❌"
                                    st.write(f"{status_icon} {email_result['name']} ({email_result['company']}) - {email_result['message']}")
                        else:
                            st.error(f"❌ {result}")
            
            with col2:
                if st.button("🧪 Test Gmail Web"):
                    with st.spinner("Opening test email in Gmail..."):
                        gmail_sender = GmailWebSender()
                        success, message = gmail_sender.open_gmail_compose(
                            {'name': 'Test User', 'email': 'mehakjuneja12@gmail.com', 'company': 'Test Company', 'city': 'Test City', 'score': 85, 'score_category': '🟢 High'},
                            "I hope this message finds you well. I'm reaching out because I noticed that Test Company manages properties in Test City - an area we've identified as having excellent potential for our property management solutions.\n\nMarket Score: 85/100 (High Priority)\n\nThis is a test email to demonstrate the Gmail web integration functionality."
                        )
                        if success:
                            st.success("✅ Test email opened in Gmail!")
                        else:
                            st.error(f"❌ {message}")
            
            with col3:
                if st.button("📋 Preview Email Template"):
                    if len(high_priority_leads) > 0:
                        sample_lead = high_priority_leads.iloc[0]
                        sample_message = sample_lead.get('outreach_message', 'Sample outreach message')
                        
                        gmail_sender = GmailWebSender()
                        preview = gmail_sender.preview_email(sample_lead.to_dict(), sample_message)
                        
                        with st.expander("📧 Email Preview"):
                            st.markdown("**Sample Email Preview:**")
                            st.markdown(f"**To:** {preview['to']}")
                            st.markdown(f"**Subject:** {preview['subject']}")
                            st.markdown("**Content:**")
                            st.markdown(preview['body'].replace('\n', '\n\n'))
            
            with col4:
                if st.button("📥 Open Gmail Inbox"):
                    gmail_sender = GmailWebSender()
                    success, message = gmail_sender.open_gmail_inbox()
                    if success:
                        st.success("✅ Gmail inbox opened!")
                    else:
                        st.error(f"❌ {message}")
        
        elif email_method == "📱 Mac Mail App":
            st.success("✅ Mac Mail App - No password required!")
            st.info("This will open your Mac's Mail app with pre-composed emails for each lead.")
            
            # Mail App controls
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📱 Open Mail App for All High-Priority Leads", type="primary"):
                    with st.spinner("Opening Mail app for high-priority leads..."):
                        mail_sender = MailAppSender()
                        success, result = mail_sender.open_bulk_emails(high_priority_leads, min_score=71)
                        
                        if success:
                            st.success(f"✅ {result['summary']}")
                            
                            # Show detailed results
                            with st.expander("📊 Mail App Results Details"):
                                for email_result in result['results']:
                                    status_icon = "✅" if email_result['success'] else "❌"
                                    st.write(f"{status_icon} {email_result['name']} ({email_result['company']}) - {email_result['message']}")
                        else:
                            st.error(f"❌ {result}")
            
            with col2:
                if st.button("🧪 Test Mail App"):
                    with st.spinner("Opening test email..."):
                        mail_sender = MailAppSender()
                        success, message = mail_sender.open_mail_app(
                            {'name': 'Test User', 'email': 'mehakjuneja12@gmail.com', 'company': 'Test Company', 'city': 'Test City', 'score': 85, 'score_category': '🟢 High'},
                            "This is a test email from Lead Enrichment App. If you received this, the Mail app integration is working!"
                        )
                        if success:
                            st.success("✅ Test email opened in Mail app!")
                        else:
                            st.error(f"❌ {message}")
            
            with col3:
                if st.button("📋 Preview Email Template"):
                    if len(high_priority_leads) > 0:
                        sample_lead = high_priority_leads.iloc[0]
                        sample_message = sample_lead.get('outreach_message', 'Sample outreach message')
                        
                        mail_sender = MailAppSender()
                        preview = mail_sender.preview_email(sample_lead.to_dict(), sample_message)
                        
                        with st.expander("📧 Email Preview"):
                            st.markdown("**Sample Email Preview:**")
                            st.markdown(f"**To:** {preview['to']}")
                            st.markdown(f"**Subject:** {preview['subject']}")
                            st.markdown("**Content:**")
                            st.markdown(preview['body'].replace('\n', '\n\n'))
        
        else:  # SMTP Email method
            # Email configuration status
            email_sender = EmailSender()
            config_status = email_sender.get_email_config_status()
            
            if config_status['configured']:
                st.success("✅ Email configuration is ready")
                
                # Email controls
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📧 Send Emails to High-Priority Leads", type="primary"):
                        with st.spinner("Sending emails to high-priority leads..."):
                            success, result = email_sender.send_bulk_emails(high_priority_leads, min_score=71)
                            
                            if success:
                                st.success(f"✅ {result['summary']}")
                                
                                # Show detailed results
                                with st.expander("📊 Email Results Details"):
                                    for email_result in result['results']:
                                        status_icon = "✅" if email_result['success'] else "❌"
                                        st.write(f"{status_icon} {email_result['name']} ({email_result['company']}) - {email_result['message']}")
                            else:
                                st.error(f"❌ {result}")
                
                with col2:
                    if st.button("🧪 Test Email Configuration"):
                        test_email = st.text_input("Enter test email address:", placeholder="test@example.com")
                        if test_email and st.button("Send Test Email"):
                            with st.spinner("Sending test email..."):
                                success, message = send_test_email(test_email)
                                if success:
                                    st.success(f"✅ Test email sent successfully to {test_email}")
                                else:
                                    st.error(f"❌ {message}")
                
                with col3:
                    if st.button("📋 Preview Email Template"):
                        if len(high_priority_leads) > 0:
                            sample_lead = high_priority_leads.iloc[0]
                            sample_message = sample_lead.get('outreach_message', 'Sample outreach message')
                            
                            with st.expander("📧 Email Preview"):
                                st.markdown("**Sample Email Preview:**")
                                st.markdown(f"**To:** {sample_lead.get('email', 'lead@company.com')}")
                                st.markdown(f"**Subject:** Property Management Solutions for {sample_lead.get('company', 'Company')} in {sample_lead.get('city', 'City')}")
                                st.markdown("**Content:**")
                                st.markdown(sample_message.replace('\n', '\n\n'))
            else:
                st.warning("⚠️ Email not configured. Please set up email settings in the Settings page.")
                st.info("Required environment variables: SENDER_EMAIL, SENDER_PASSWORD")
    else:
        st.info("ℹ️ No high-priority leads found (score ≥ 71). Add more leads or adjust scoring criteria.")

def show_settings():
    st.header("⚙️ Settings")
    
    # LLM Settings
    st.subheader("🤖 AI Message Generation")
    use_llm = st.checkbox(
        "Use AI (OpenAI) for outreach message generation", 
        value=st.session_state.use_llm,
        help="Enable AI-powered personalized message generation based on weather, demographics, and market insights"
    )
    st.session_state.use_llm = use_llm
    
    if use_llm:
        st.success("✅ AI message generation enabled")
        st.info("Messages will be generated using OpenAI GPT-3.5-turbo for maximum personalization")
    else:
        st.info("📝 Using template-based message generation")
    
    st.markdown("---")
    
    # Email Configuration
    st.subheader("📧 Email Configuration")
    email_sender = EmailSender()
    config_status = email_sender.get_email_config_status()
    
    if config_status['configured']:
        st.success("✅ Email configuration is ready")
        st.info(f"**Sender:** {config_status['sender_name']} <{config_status['sender_email']}>")
        st.info(f"**SMTP Server:** {config_status['smtp_server']}:{config_status['smtp_port']}")
        
        # Test email configuration
        if st.button("🧪 Test Email Configuration"):
            with st.spinner("Testing email configuration..."):
                success, message = test_email_configuration()
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    else:
        st.warning("⚠️ Email not configured")
        st.info("Add the following to your .env file:")
        st.code("""
# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Sales Team
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
        """)
        
        st.info("**Note:** For Gmail, use an App Password instead of your regular password. Enable 2FA and generate an App Password in your Google Account settings.")
    
    st.markdown("---")
    
    st.subheader("API Configuration")
    st.info("Add your API keys to the .env file in the project root directory.")
    
    # Check if .env file exists
    env_path = "/Users/mehakjuneja/Documents/EliseAI/.env"
    if os.path.exists(env_path):
        st.success("✅ .env file found")
        
        # Test API connections
        st.subheader("API Connection Test")
        if st.button("Test API Connections"):
            try:
                from utils.api_calls import test_api_connections
                results = test_api_connections()
                
                for api, status in results.items():
                    if status:
                        st.success(f"✅ {api}: Connected")
                    else:
                        st.error(f"❌ {api}: Failed")
                
                # Test OpenAI API if enabled
                if st.session_state.use_llm:
                    try:
                        from utils.outreach import generate_llm_outreach_message
                        # Test with sample data
                        test_message = generate_llm_outreach_message(
                            "Test User", "Test Company", "San Francisco", "CA",
                            "sunny", 70, 75000, 50, 870000, "high rental market"
                        )
                        if test_message:
                            st.success("✅ OpenAI API: Connected")
                        else:
                            st.error("❌ OpenAI API: Failed")
                    except Exception as e:
                        st.error(f"❌ OpenAI API: {str(e)}")
                        
            except Exception as e:
                st.error(f"Error testing APIs: {str(e)}")
    else:
        st.warning("⚠️ .env file not found. Please create one with your API keys.")
        st.code("""
# Create a .env file with the following content:
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATAUSA_API_KEY=your_datausa_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
""")
    
    st.subheader("About")
    st.info("""
    **Lead Enrichment & Outreach Assistant**
    
    This app enriches inbound leads using:
    - OpenWeather API for weather data
    - DataUSA API for demographic information
    - OpenAI API for AI-powered message generation
    
    Features:
    - Automatic lead scoring
    - AI-powered personalized outreach generation
    - Real weather and demographic data
    - Interactive dashboard
    - CSV/Excel export
    - Persistent data storage
    """)

def generate_insights(enriched_data):
    """Generate insights based on enriched data"""
    insights = []
    
    percent_renters = enriched_data.get('percent_renters', 0)
    median_income = enriched_data.get('median_income', 0)
    temperature = enriched_data.get('temperature', 0)
    
    if percent_renters > 50:
        insights.append("high rental market")
    elif percent_renters > 30:
        insights.append("moderate rental market")
    else:
        insights.append("low rental market")
    
    if median_income > 75000:
        insights.append("affluent area")
    elif median_income > 50000:
        insights.append("middle-income area")
    else:
        insights.append("budget-conscious area")
    
    if temperature > 80:
        insights.append("warm climate")
    elif temperature < 40:
        insights.append("cool climate")
    else:
        insights.append("temperate climate")
    
    return ", ".join(insights)

if __name__ == "__main__":
    main()
