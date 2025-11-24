# Lead Enrichment & Outreach Assistant

A Streamlit web app that automates and augments the inbound lead process by enriching manually entered lead data using public APIs, scoring the leads, and generating personalized outreach messages for sales reps.

## 🚀 Features

- **📝 Manual Input Form**: Enter lead information (name, email, company, property address, city, state, country)
- **🔍 API Enrichment**: 
  - OpenWeather API for real-time weather data
  - DataUSA API for demographics (median income, population, % renters)
- **📊 Advanced Lead Scoring**: 0-100 score with realistic variance based on rental market, income, and weather
- **🤖 AI-Powered Outreach**: LLM-generated personalized email messages using OpenAI GPT-3.5-turbo
- **📧 Automated Email Campaigns**: Send personalized emails to high-priority leads (score ≥ 71)
- **💡 Smart Personalization**: Messages adapt to local weather, demographics, and market conditions
- **📈 Interactive Dashboard**: View and filter enriched leads with detailed analytics
- **📥 Export Functionality**: Download results as CSV or Excel
- **💾 Persistent Storage**: Leads saved across sessions with automatic data persistence

## Quick Start

### Option 1: Use the Startup Script (Recommended)
```bash
./start_app.sh
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip3 install -r requirements.txt
```

2. **API Keys Setup** (Optional)
The app comes with an `env_template.txt` file. Copy it to `.env` and fill in your API keys:
```env
# OpenWeather API Key (for real weather data)
# Get your free API key at: https://openweathermap.org/api
OPENWEATHER_API_KEY=your_openweather_api_key_here

# DataUSA API Key (optional - basic usage doesn't require a key)
# Get your API key at: https://datausa.io/about/api/
DATAUSA_API_KEY=your_datausa_api_key_here

# OpenAI API Key (for AI-powered message generation)
# Get your API key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (for automated outreach)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
SENDER_NAME=Sales Team
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

3. **Run the Application**
```bash
streamlit run app.py
```

### **Quick Email Setup (Optional)**
For automated email campaigns to high-priority leads:

1. **Copy Environment Template**
```bash
cp env_template.txt .env
```

2. **Configure Email Settings**
Edit `.env` file with your email credentials:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Sales Team
```

3. **Test Email Configuration**
- Go to Settings page in the app
- Click "🧪 Test Email Configuration"
- Send a test email to verify setup

4. **Send Campaign Emails**
- Go to Dashboard page
- Click "📧 Send Emails to High-Priority Leads"
- View delivery results and follow up

### Option 3: Try the Demo First
```bash
python3 demo.py              # Basic functionality demo
python3 demo_llm.py          # AI vs Template message comparison
```

## 📁 Project Structure

```
LeadEnrichment/
├── app.py                          # Streamlit main application
├── demo.py                         # Basic functionality demo
├── demo_llm.py                     # AI vs Template message comparison
├── test_app.py                     # Test suite
├── start_app.sh                    # Startup script
├── requirements.txt                # Python dependencies
├── env_template.txt                # Environment variables template
├── comprehensive_lead_list.txt     # 40+ sample leads for testing
├── sample_leads_diverse.txt        # Diverse lead examples
├── SCORING_LOGIC.md               # Detailed scoring algorithm explanation
├── SCORING_INPUTS_BREAKDOWN.md    # Input specifications and methodology
├── utils/
│   ├── api_calls.py               # OpenWeather + DataUSA enrichment logic
│   ├── scoring.py                 # Advanced lead scoring algorithm
│   ├── outreach.py                # AI-powered outreach message generation
│   └── email_sender.py            # Automated email campaigns for high-priority leads
├── data/
│   ├── leads.csv                  # Persistent lead storage
│   └── sample_leads.csv           # Sample data for testing
└── README.md                      # This file
```

## 📊 Lead Scoring Algorithm

The lead scoring system uses a sophisticated weighted formula combining three key factors:

### **Scoring Components (100 points total)**

#### **1. Rental Market Density (40 points max)**
- **60%+ renters:** 40 points (Excellent) - Premium rental markets
- **50-59% renters:** 35 points (High) - Strong rental markets  
- **40-49% renters:** 25 points (Moderate) - Average rental markets
- **30-39% renters:** 15 points (Low) - Weak rental markets
- **<30% renters:** 5 points (Very Low) - Minimal rental market

#### **2. Median Household Income (30 points max)**
- **$80k+ income:** 30 points (High) - Affluent areas
- **$70-79k income:** 25 points (Above Average) - Upper-middle class
- **$60-69k income:** 20 points (Average) - Middle class
- **$50-59k income:** 15 points (Below Average) - Lower-middle class
- **$40-49k income:** 10 points (Low) - Working class
- **<$40k income:** 5 points (Very Low) - Economically challenged

#### **3. Weather Conditions (20 points max)**
- **65-75°F:** 20 points (Optimal) - Perfect conditions
- **60-64°F or 76-80°F:** 15 points (Good) - Comfortable conditions
- **55-59°F or 81-85°F:** 10 points (Moderate) - Acceptable conditions
- **50-54°F or 86-90°F:** 5 points (Poor) - Challenging conditions
- **<50°F or >90°F:** 0 points (Extreme) - Difficult conditions

### **Score Categories:**
- **🟢 High (71-100):** Premium leads with excellent market conditions
- **🟡 Medium (41-70):** Good leads with solid market potential
- **🔴 Low (0-40):** Challenging leads requiring more effort

### **Example Scores:**
- **San Francisco:** 85 points (55% renters + $95k income + 65°F)
- **Detroit:** 25 points (35% renters + $45k income + 45°F)
- **Austin:** 65 points (45% renters + $65k income + 75°F)

## API Usage

### OpenWeather API
- Provides current weather conditions and temperature
- Free tier: 1,000 calls/day
- Sign up at: https://openweathermap.org/api

### DataUSA API
- Provides demographic and economic data
- Free tier available
- Sign up at: https://datausa.io/about/api/

### Email Configuration
- **Gmail SMTP**: Use App Password (not regular password)
- **Outlook/Hotmail**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **Custom SMTP**: Configure your own server

## 📧 Email Campaign Features

### **Automated High-Priority Lead Outreach**
The app automatically identifies and emails leads with scores ≥ 71 (High Priority):

- **🎯 Smart Targeting**: Only emails the highest-scoring leads
- **📧 Professional Templates**: HTML emails with company branding
- **💬 Personalized Content**: Each email includes lead-specific data
- **📊 Delivery Tracking**: Success/failure reporting for each email
- **🔄 Bulk Sending**: Send to multiple leads simultaneously

### **Email Template Features**
- **Responsive Design**: Works on desktop and mobile
- **Company Branding**: Customizable colors and styling
- **Score Integration**: Shows lead score and category
- **Call-to-Action**: Direct scheduling links
- **Unsubscribe Support**: Built-in unsubscribe functionality

### **Email Configuration Options**
```env
# Gmail (Recommended)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Sales Team
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Outlook/Hotmail
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### **Gmail Setup Instructions**
1. Enable 2-Factor Authentication in your Google Account
2. Go to Google Account Settings → Security → App Passwords
3. Generate a new App Password for "Mail"
4. Use the App Password (not your regular password) in `SENDER_PASSWORD`

## 🎯 Usage

### **Demo Mode**
The app works with realistic mock data when no API keys are provided, making it perfect for testing:
```bash
python3 demo.py              # Basic functionality demo
python3 demo_llm.py          # AI vs Template message comparison
```

### **Full App Usage**
1. **📝 Add New Lead**: Fill out the form with lead information
2. **🔍 Automatic Enrichment**: The app fetches real-time weather and demographic data
3. **📊 Lead Scoring**: View the calculated score with detailed breakdown
4. **💬 Outreach Generation**: Copy the AI-generated personalized message
5. **📧 Email Campaigns**: Automatically send emails to high-priority leads (score ≥ 71)
6. **📈 Dashboard**: View all leads with filtering, analytics, and export options

### **Sample Leads**
Use the comprehensive lead list for testing:
- **40+ realistic leads** with actual property addresses
- **Diverse market conditions** (high, medium, low scores)
- **Geographic variety** (US cities, international options)
- **Specialized markets** (luxury, student housing, etc.)

### **Email Campaign Workflow**
1. **📊 Review High-Priority Leads**: Dashboard shows leads with score ≥ 71
2. **⚙️ Configure Email Settings**: Set up SMTP in Settings page
3. **🧪 Test Configuration**: Send test email to verify setup
4. **📧 Launch Campaign**: Send bulk emails to all high-priority leads
5. **📈 Monitor Results**: View delivery success/failure reports
6. **📋 Follow Up**: Track responses and schedule calls

### **Testing**
Run the test suite to verify everything works:
```bash
python3 test_app.py
```

## 🛠️ Customization

- **Scoring Algorithm**: Modify weights and thresholds in `utils/scoring.py`
- **Outreach Templates**: Customize message templates in `utils/outreach.py`
- **API Integrations**: Add new data sources in `utils/api_calls.py`
- **UI/UX**: Update the interface in `app.py`
- **Sample Data**: Add more test leads in `comprehensive_lead_list.txt`

## 📚 Documentation

- **`SCORING_LOGIC.md`**: Detailed explanation of the scoring algorithm and business rationale
- **`SCORING_INPUTS_BREAKDOWN.md`**: Complete input specifications and methodology
- **`comprehensive_lead_list.txt`**: 40+ sample leads for testing different scenarios

## 🔧 Troubleshooting

### **General Issues**
- **API Errors**: Check your API keys in the `.env` file
- **No Data**: Some cities may not have complete demographic data (app uses realistic fallbacks)
- **Slow Loading**: API calls may take a few seconds to complete
- **Scoring Issues**: Verify the scoring algorithm in `utils/scoring.py`

### **Email Issues**
- **Authentication Failed**: Verify your email credentials in `.env`
- **Gmail Issues**: Use App Password, not regular password
- **SMTP Errors**: Check SMTP server and port settings
- **No High-Priority Leads**: Add more leads or adjust scoring criteria
- **Email Not Sending**: Test configuration in Settings page first

### **Common Email Solutions**
```bash
# Gmail: Enable 2FA and use App Password
# Outlook: Use your regular password
# Yahoo: May require App Password
# Custom SMTP: Verify server settings with your provider
```

## 🎯 Key Improvements

- **Realistic Scoring**: Updated algorithm provides better variance (25-85 point range)
- **Tiered Scoring**: More granular scoring tiers for better lead differentiation
- **Automated Email Campaigns**: Send personalized emails to high-priority leads automatically
- **Professional Email Templates**: HTML email templates with company branding
- **Comprehensive Testing**: 40+ sample leads covering diverse market conditions
- **Better Documentation**: Detailed explanations of scoring logic and inputs

## 💼 Business Value

### **Lead Enrichment & Scoring**
- **Data-Driven Decisions**: Real-time market data for informed lead prioritization
- **Time Savings**: Automated enrichment eliminates manual research
- **Quality Focus**: Concentrate efforts on highest-potential leads (score ≥ 71)

### **Automated Outreach**
- **Scalable Communication**: Send personalized emails to multiple leads simultaneously
- **Professional Presentation**: Branded emails with professional presentation
- **Efficiency Gains**: No manual email composition or sending required
- **Response Tracking**: Monitor delivery success and follow up effectively

### **ROI Benefits**
- **Higher Conversion Rates**: Target only the best leads with personalized outreach
- **Reduced Sales Cycle**: Automated initial contact speeds up the sales process
- **Cost Efficiency**: Eliminate manual lead research and email composition time
- **Scalable Growth**: Handle increasing lead volumes without proportional resource increases

## 📄 License

This project is open source and available for use by any company.
