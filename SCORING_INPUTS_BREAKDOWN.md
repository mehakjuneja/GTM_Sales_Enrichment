# EliseAI Lead Scoring: Input Details & Methodology

## 📋 Input Requirements

### **Primary Inputs (Required)**
The scoring system requires **3 specific data points** to calculate a lead score:

1. **`percent_renters`** (float) - Percentage of renters in the area
2. **`median_income`** (float) - Median household income in the area  
3. **`temperature`** (float) - Current temperature in Fahrenheit

---

## 🔄 Data Flow Process

### **Step 1: User Input**
```
User provides: City, State, Country
Example: "San Francisco", "CA", "USA"
```

### **Step 2: API Enrichment**
The system automatically enriches the lead data by calling external APIs:

#### **Weather Data Source: OpenWeather API**
- **Input:** City, State, Country
- **Output:** Current temperature, weather description, humidity, wind speed
- **Key Field:** `temperature` (Fahrenheit)

#### **Demographic Data Source: DataUSA API**
- **Input:** City, State
- **Output:** Population, median income, rental statistics
- **Key Fields:** `median_income`, `percent_renters`

### **Step 3: Fallback Data**
If APIs fail, the system uses realistic estimates based on:
- City-specific demographic patterns
- State-level economic data
- Historical weather patterns

---

## 📊 Detailed Input Specifications

### **1. Percent Renters (percent_renters)**

**Data Type:** `float`  
**Range:** 0.0 - 100.0  
**Unit:** Percentage  
**Source:** DataUSA API or realistic estimates

**How it's calculated:**
- **API Method:** DataUSA provides housing unit data by tenure (owner vs. renter occupied)
- **Formula:** `(Renter Occupied Units / Total Housing Units) * 100`
- **Fallback:** City-specific rental percentages based on real market data

**Example Values:**
- San Francisco: ~55% (High rental market)
- Detroit: ~35% (Low rental market)
- Miami: ~60% (Very high rental market)

**Scoring Impact:**
```python
if percent_renters >= 60:
    rental_score = 40  # Excellent (40 points)
elif percent_renters >= 50:
    rental_score = 35  # High (35 points)
elif percent_renters >= 40:
    rental_score = 25  # Moderate (25 points)
elif percent_renters >= 30:
    rental_score = 15  # Low (15 points)
else:
    rental_score = 5   # Very Low (5 points)
```

---

### **2. Median Income (median_income)**

**Data Type:** `float`  
**Range:** $20,000 - $150,000+  
**Unit:** US Dollars (annual)  
**Source:** DataUSA API or state-level estimates

**How it's calculated:**
- **API Method:** DataUSA provides household income distribution data
- **Formula:** Median of all household incomes in the area
- **Fallback:** State-level median income data

**Example Values:**
- San Francisco: ~$95,000 (High income)
- Detroit: ~$45,000 (Low income)
- Austin: ~$65,000 (Average income)

**Scoring Impact:**
```python
if median_income >= 80000:
    income_score = 30  # High (30 points)
elif median_income >= 70000:
    income_score = 25  # Above Average (25 points)
elif median_income >= 60000:
    income_score = 20  # Average (20 points)
elif median_income >= 50000:
    income_score = 15  # Below Average (15 points)
elif median_income >= 40000:
    income_score = 10  # Low (10 points)
else:
    income_score = 5   # Very Low (5 points)
```

---

### **3. Temperature (temperature)**

**Data Type:** `float`  
**Range:** -20°F to 120°F  
**Unit:** Fahrenheit  
**Source:** OpenWeather API or realistic estimates

**How it's calculated:**
- **API Method:** OpenWeather provides current weather conditions
- **Formula:** Real-time temperature from weather stations
- **Fallback:** City-specific average temperatures based on climate data

**Example Values:**
- San Francisco: ~65°F (Optimal)
- Phoenix: ~85°F (Moderate)
- Buffalo: ~35°F (Extreme)

**Scoring Impact:**
```python
if 65 <= temperature <= 75:
    temp_score = 20  # Optimal (20 points)
elif 60 <= temperature < 65 or 75 < temperature <= 80:
    temp_score = 15  # Good (15 points)
elif 55 <= temperature < 60 or 80 < temperature <= 85:
    temp_score = 10  # Moderate (10 points)
elif 50 <= temperature < 55 or 85 < temperature <= 90:
    temp_score = 5   # Poor (5 points)
else:
    temp_score = 0   # Extreme (0 points)
```

---

## 🧮 Scoring Calculation Process

### **Step-by-Step Calculation:**

1. **Input Validation:**
   ```python
   # Ensure inputs are valid numbers
   percent_renters = float(percent_renters)
   median_income = float(median_income)
   temperature = float(temperature)
   ```

2. **Rental Score Calculation:**
   ```python
   # Determine rental market tier
   if percent_renters >= 60:
       rental_score = 40
   elif percent_renters >= 50:
       rental_score = 35
   # ... etc
   ```

3. **Income Score Calculation:**
   ```python
   # Determine income tier
   if median_income >= 80000:
       income_score = 30
   elif median_income >= 70000:
       income_score = 25
   # ... etc
   ```

4. **Temperature Score Calculation:**
   ```python
   # Determine weather tier
   if 65 <= temperature <= 75:
       temp_score = 20
   elif 60 <= temperature < 65 or 75 < temperature <= 80:
       temp_score = 15
   # ... etc
   ```

5. **Total Score Calculation:**
   ```python
   total_score = rental_score + income_score + temp_score
   total_score = max(0, min(total_score, 100))  # Ensure 0-100 range
   return round(total_score)
   ```

---

## 📈 Score Categories

### **Final Score Ranges:**
- **🟢 High (71-100 points):** Premium leads with excellent market conditions
- **🟡 Medium (41-70 points):** Good leads with solid market potential
- **🔴 Low (0-40 points):** Challenging leads requiring more effort

---

## 🔍 Example Calculations

### **Example 1: San Francisco**
```
Inputs:
- percent_renters: 55.0
- median_income: 95000.0
- temperature: 65.0

Calculation:
- Rental Score: 55% → High tier → 35 points
- Income Score: $95k → High tier → 30 points
- Temperature Score: 65°F → Optimal tier → 20 points

Total Score: 35 + 30 + 20 = 85 points
Category: 🟢 High
```

### **Example 2: Detroit**
```
Inputs:
- percent_renters: 35.0
- median_income: 45000.0
- temperature: 45.0

Calculation:
- Rental Score: 35% → Low tier → 15 points
- Income Score: $45k → Low tier → 10 points
- Temperature Score: 45°F → Extreme tier → 0 points

Total Score: 15 + 10 + 0 = 25 points
Category: 🔴 Low
```

---

## 🛠️ Technical Implementation

### **Function Signature:**
```python
def calculate_lead_score(percent_renters, median_income, temperature):
    """
    Calculate lead score based on multiple factors
    
    Args:
        percent_renters (float): Percentage of renters in the area
        median_income (float): Median income in the area
        temperature (float): Current temperature in Fahrenheit
    
    Returns:
        int: Lead score from 0-100
    """
```

### **Data Sources:**
1. **OpenWeather API:** Real-time weather data
2. **DataUSA API:** Demographic and economic data
3. **Fallback Data:** Realistic estimates based on city/state patterns

### **Error Handling:**
- API failures fall back to realistic estimates
- Invalid inputs are handled gracefully
- Score is always bounded between 0-100

---

## 📋 Input Data Quality

### **Data Accuracy:**
- **Weather:** Real-time, highly accurate
- **Demographics:** Census-based, updated annually
- **Fallback:** Based on real market research

### **Data Freshness:**
- **Weather:** Updated every API call (real-time)
- **Demographics:** Updated annually from census data
- **Fallback:** Based on latest available data

This scoring system provides a robust, data-driven approach to lead evaluation that prioritizes markets with the highest potential for EliseAI's property management services.
