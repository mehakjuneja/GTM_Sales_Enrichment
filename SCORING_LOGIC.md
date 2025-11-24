# EliseAI Lead Scoring Logic & Business Rationale

## Overview
The lead scoring system evaluates potential property management clients based on three key factors that directly impact the likelihood of success and profitability for EliseAI's services.

## Scoring Framework (Total: 100 points)

### 1. Rental Market Density (40 points max) - **PRIMARY FACTOR**

**Weight:** 40% of total score  
**Rationale:** This is the most critical factor because it directly measures market opportunity.

#### Scoring Tiers:
- **60%+ renters:** 40 points (Excellent) - Premium rental markets
- **50-59% renters:** 35 points (High) - Strong rental markets  
- **40-49% renters:** 25 points (Moderate) - Average rental markets
- **30-39% renters:** 15 points (Low) - Weak rental markets
- **<30% renters:** 5 points (Very Low) - Minimal rental market

#### Business Logic:
- **Market Size:** Higher rental percentage = larger addressable market
- **Service Demand:** More renters = higher demand for property management services
- **Competition:** High-rental areas often have established property management ecosystems
- **Growth Potential:** Areas with growing rental populations offer expansion opportunities

**Examples:**
- San Francisco (55% renters) = 35 points
- Detroit (35% renters) = 15 points

---

### 2. Median Household Income (30 points max) - **SECONDARY FACTOR**

**Weight:** 30% of total score  
**Rationale:** Income level directly impacts ability to pay for premium property management services.

#### Scoring Tiers:
- **$80k+ income:** 30 points (High) - Affluent areas
- **$70-79k income:** 25 points (Above Average) - Upper-middle class
- **$60-69k income:** 20 points (Average) - Middle class
- **$50-59k income:** 15 points (Below Average) - Lower-middle class
- **$40-49k income:** 10 points (Low) - Working class
- **<$40k income:** 5 points (Very Low) - Economically challenged

#### Business Logic:
- **Service Affordability:** Higher income = more disposable income for property management
- **Service Sophistication:** Affluent areas demand higher-quality, tech-enabled services
- **Pricing Power:** Higher income areas can support premium pricing
- **Customer Lifetime Value:** Wealthier clients typically have higher LTV
- **Payment Reliability:** Higher income = lower payment default risk

**Examples:**
- San Francisco ($95k income) = 30 points
- Detroit ($45k income) = 10 points

---

### 3. Weather Conditions (20 points max) - **TERTIARY FACTOR**

**Weight:** 20% of total score  
**Rationale:** Weather affects resident engagement, property maintenance needs, and service delivery.

#### Scoring Tiers:
- **65-75°F:** 20 points (Optimal) - Perfect conditions
- **60-64°F or 76-80°F:** 15 points (Good) - Comfortable conditions
- **55-59°F or 81-85°F:** 10 points (Moderate) - Acceptable conditions
- **50-54°F or 86-90°F:** 5 points (Poor) - Challenging conditions
- **<50°F or >90°F:** 0 points (Extreme) - Difficult conditions

#### Business Logic:
- **Resident Engagement:** Comfortable weather = higher resident satisfaction and engagement
- **Maintenance Costs:** Extreme weather increases property maintenance needs
- **Service Delivery:** Weather affects on-site service delivery and inspections
- **Seasonal Patterns:** Moderate climates have more consistent service demand
- **Technology Adoption:** Comfortable weather areas often have higher tech adoption

**Examples:**
- San Francisco (65°F) = 20 points (Optimal)
- Phoenix (85°F) = 10 points (Moderate)
- Buffalo (35°F) = 0 points (Extreme)

---

## Lead Categories & Business Implications

### 🟢 High Score (71-100 points) - **PREMIUM LEADS**
**Characteristics:** High rental density + High income + Optimal weather
**Business Value:**
- Highest conversion probability
- Premium pricing potential
- High customer lifetime value
- Strong word-of-mouth potential
- Low churn risk

**Target Markets:** San Francisco, Seattle, Boston, New York

### 🟡 Medium Score (41-70 points) - **GOOD LEADS**
**Characteristics:** Moderate rental density + Average income + Acceptable weather
**Business Value:**
- Solid conversion potential
- Standard pricing
- Moderate customer lifetime value
- Good growth potential
- Manageable churn risk

**Target Markets:** Austin, Denver, Portland, Nashville

### 🔴 Low Score (0-40 points) - **CHALLENGING LEADS**
**Characteristics:** Low rental density + Low income + Poor weather
**Business Value:**
- Lower conversion probability
- Competitive pricing required
- Lower customer lifetime value
- Higher churn risk
- May require more sales effort

**Target Markets:** Detroit, Buffalo, smaller rural areas

---

## Additional Considerations (Not Currently Scored)

### Potential Future Scoring Factors:

1. **Property Size & Type (0-15 points)**
   - Large apartment complexes vs. single-family homes
   - Newer properties vs. older properties
   - Luxury vs. affordable housing

2. **Local Economic Indicators (0-10 points)**
   - Job growth rate
   - Unemployment rate
   - Population growth
   - Business development

3. **Competition Density (0-10 points)**
   - Number of existing property management companies
   - Market saturation level
   - Competitive pricing pressure

4. **Technology Adoption (0-10 points)**
   - Internet penetration
   - Mobile app usage
   - PropTech adoption rate

5. **Regulatory Environment (0-5 points)**
   - Landlord-tenant laws
   - Property management licensing requirements
   - Tax implications

---

## Scoring Algorithm Implementation

```python
def calculate_lead_score(percent_renters, median_income, temperature):
    # Rental Market Score (0-40 points)
    if percent_renters >= 60:
        rental_score = 40
    elif percent_renters >= 50:
        rental_score = 35
    elif percent_renters >= 40:
        rental_score = 25
    elif percent_renters >= 30:
        rental_score = 15
    else:
        rental_score = 5
    
    # Income Score (0-30 points)
    if median_income >= 80000:
        income_score = 30
    elif median_income >= 70000:
        income_score = 25
    elif median_income >= 60000:
        income_score = 20
    elif median_income >= 50000:
        income_score = 15
    elif median_income >= 40000:
        income_score = 10
    else:
        income_score = 5
    
    # Temperature Score (0-20 points)
    if 65 <= temperature <= 75:
        temp_score = 20
    elif 60 <= temperature < 65 or 75 < temperature <= 80:
        temp_score = 15
    elif 55 <= temperature < 60 or 80 < temperature <= 85:
        temp_score = 10
    elif 50 <= temperature < 55 or 85 < temperature <= 90:
        temp_score = 5
    else:
        temp_score = 0
    
    return rental_score + income_score + temp_score
```

---

## Business Assumptions & Rationale

### Why These Factors Matter for EliseAI:

1. **Rental Market Density (40%):** 
   - Directly correlates with service demand
   - Higher density = more potential customers
   - Easier to achieve economies of scale

2. **Income Level (30%):**
   - Affects pricing power and service sophistication
   - Higher income = willingness to pay for premium services
   - Reduces payment collection issues

3. **Weather (20%):**
   - Impacts resident satisfaction and engagement
   - Affects property maintenance costs
   - Influences service delivery efficiency

### Market Research Basis:
- Property management industry typically targets 40%+ rental markets
- Premium services require $60k+ household income
- Moderate climates (60-80°F) show highest resident satisfaction
- Tech adoption correlates with income and weather comfort

This scoring system prioritizes markets where EliseAI can:
- Achieve high conversion rates
- Command premium pricing
- Deliver consistent service quality
- Build sustainable, long-term customer relationships
