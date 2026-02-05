# 🌍 Carbon Footprint Prediction System

A machine learning-powered web application that predicts personal daily carbon footprints and provides intelligent, personalized action plans to reduce environmental impact.

## 🎯 Features

### Dual-Output ML System
- **Random Forest Regression**: Predicts exact carbon footprint values (kg CO₂/day)
- **Rule-Based Classification**: Categorizes impact levels (Low/Medium/High)
- **Post-Processing Correction**: Ensures food ordering constraints (Non-Veg ≥ Mixed ≥ Veg)

### Three-Tier Intelligent Tip Generation Engine

#### Level 1: Priority-Based Rule Tips
Context-aware actionable advice that considers actual input values:
- Only suggests changes where improvement is possible
- Prioritizes tips based on input magnitudes
- Provides specific, measurable recommendations

#### Level 2: What-If Analysis
Intelligent simulations showing potential CO₂ savings by making lifestyle changes:
- Switch transport modes (with calculated savings)
- Change diet types (respecting food ordering)
- Reduce screen time (specific hour reductions)
- Compare alternative scenarios side-by-side

#### Level 3: Feature Importance Analysis
ML-powered insights identifying which factors contribute most to your carbon footprint:
- Data-driven recommendations based on model weights
- Personalized to your specific input profile

### Interactive Web Interface
Built with Streamlit featuring:
- 📊 Real-time carbon footprint visualization with gauge charts
- 🎨 Centered, user-friendly input layout
- 💡 Three-tab personalized action plan display
- 🔄 Scenario comparison (Best/Average/Worst cases)
- ⚡ Instant predictions with session state management

## 📋 Dataset

**Source**: [Kaggle - Personal Carbon Footprint Behavior Dataset](https://www.kaggle.com/datasets/sonalshinde123/personal-carbon-footprint-behavior-dataset)

**Dataset Size**: 1,400 records

**Input Features (5 total):**

| Feature | Type | Range/Values | Description |
|---------|------|--------------|-------------|
| `transport_mode` | Categorical | Car, Bus, Bike, EV, Walk | Primary mode of transportation |
| `distance_km` | Numerical | 0-100 km (step 0.5) | Daily travel distance |
| `electricity_kwh` | Numerical | 0-20 kWh (step 0.5) | **Daily** electricity usage |
| `food_type` | Categorical | Non-Veg, Mixed, Veg | Dietary preference |
| `screen_time_hours` | Numerical | 0-24 hours (step 0.5) | Daily screen time |

**Target Variables:**
- `carbon_footprint_kg`: Carbon footprint value in kg CO₂/day (regression)
- `carbon_impact_level`: Low/Medium/High classification

**Removed Features**: `user_id`, `day_type`, `waste_generated_kg`, `eco_actions`, `renewable_usage_pct`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**:
- streamlit==1.54.0
- pandas==2.3.3
- numpy==2.4.1
- scikit-learn==1.8.0
- plotly==6.5.2
- kagglehub==0.4.2

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Download the dataset from Kaggle (1,400 records)
- Preprocess and clean the data (remove 5 unnecessary columns)
- Apply one-hot encoding to categorical features
- Train the Random Forest model with optimized hyperparameters
- Save the model to `models/carbon_footprint_model.pkl`
- Save preprocessor config to `models/preprocessor.pkl`

**Training Output**:
```
✓ Loaded 1400 records
✓ Preprocessed data: 10 features
✓ Training set: 1120 samples
✓ Test set: 280 samples
✓ Model R² Score: 0.5263
✓ RMSE: 1.8904 kg CO₂
✓ MAE: 1.5060 kg CO₂
```

### 3. Run the Web Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Capestone project/
│
├── app.py                      # Streamlit web application (12.95 KB)
├── train_model.py              # ML model training script (8.15 KB)
├── data_loader.py              # Data loading and preprocessing (5.18 KB)
├── tip_generator.py            # Three-tier tip generation engine (11.49 KB)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── models/                     # Saved models (created after training)
    ├── carbon_footprint_model.pkl      # Trained Random Forest model
    └── preprocessor.pkl                # Feature column configuration
```

## 🎓 How It Works

### 1. Data Preprocessing (`data_loader.py`)
```python
# Remove unnecessary columns
columns_to_remove = ['user_id', 'day_type', 'waste_generated_kg', 
                     'eco_actions', 'renewable_usage_pct']

# One-hot encoding for categorical features
X_encoded = pd.get_dummies(X, columns=['transport_mode', 'food_type'])

# Resulting feature columns (10 total):
# - distance_km, electricity_kwh, screen_time_hours
# - transport_mode_Bike, transport_mode_Bus, transport_mode_Car, 
#   transport_mode_EV, transport_mode_Walk
# - food_type_Mixed, food_type_Non-Veg, food_type_Veg
```

### 2. Model Training (`train_model.py`)

**Algorithm**: Random Forest Regressor

**Optimized Hyperparameters**:
```python
n_estimators = 150           # Number of trees
max_depth = 12               # Maximum tree depth
min_samples_split = 10       # Min samples to split node
min_samples_leaf = 4         # Min samples in leaf node
max_features = 'sqrt'        # Features per split
random_state = 42            # Reproducibility
```

**Training Split**: 80% train (1,120 samples), 20% test (280 samples)

**Food Ordering Correction**:
```python
def predict_footprint_corrected(self, X):
    """Ensures Non-Veg ≥ Mixed ≥ Veg ordering"""
    predictions = {}
    
    # Generate predictions for all food types
    for food in ['Veg', 'Mixed', 'Non-Veg']:
        X_food = X.copy()
        X_food[food_columns] = 0
        X_food[f'food_type_{food}'] = 1
        predictions[food] = model.predict(X_food)[0]
    
    # Enforce ordering: Non-Veg ≥ Mixed ≥ Veg
    predictions['Mixed'] = max(predictions['Mixed'], predictions['Veg'])
    predictions['Non-Veg'] = max(predictions['Non-Veg'], predictions['Mixed'])
    
    return predictions[selected_food_type]
```

### 3. Prediction Flow
```
User Input (5 features)
    ↓
Data Preprocessing (one-hot encoding → 10 features)
    ↓
Random Forest Prediction (150 trees)
    ↓
Food Ordering Correction (if needed)
    ↓
Impact Classification (Low/Medium/High)
    ↓
Three-Tier Tip Generation
    ↓
Display Results (gauge chart + 3 tabs)
```

### 4. Tip Generation System (`tip_generator.py`)

**Level 1 - Priority-Based Rules**:
```python
# Prioritize tips based on actual input values
if distance_km > 50:
    priority_tips.append("High travel distance detected...")
if electricity_kwh > 15:
    priority_tips.append("Very high electricity usage...")
if food_type == 'Non-Veg':
    priority_tips.append("Consider reducing meat consumption...")
```

**Level 2 - What-If Analysis**:
```python
# Calculate savings for alternative choices
current_footprint = model.predict(current_input)

# Test transport alternatives
for alt_transport in ['Bus', 'Bike', 'Walk', 'EV']:
    alt_input = current_input.copy()
    alt_input['transport_mode'] = alt_transport
    alt_footprint = model.predict(alt_input)
    savings = current_footprint - alt_footprint
    if savings > 0.5:  # Significant savings
        tips.append(f"Switch to {alt_transport}: Save {savings:.2f} kg CO₂/day")
```

**Level 3 - Feature Importance**:
```python
# Extract feature importance from trained model
importances = model.feature_importances_
# Top features:
# 1. electricity_kwh: 31.09%
# 2. food_type_Non-Veg: 21.71%
# 3. food_type_Veg: 15.86%
# 4. distance_km: 10.44%
```

## 📊 Model Performance

### Validation Results

**Performance Metrics**:
- **R² Score**: 0.5263 (52.63% variance explained)
- **RMSE**: 1.8904 kg CO₂/day
- **MAE**: 1.5060 kg CO₂/day

**Prediction Range**: 3.70 - 12.92 kg CO₂/day

**Why R² = 0.52 is acceptable**:
- Human behavior data has inherent variability
- Model captures major patterns correctly
- All predictions are physically plausible
- Post-processing ensures logical consistency

### Comprehensive Testing
- **Total Combinations Tested**: 6,057,135 (all possible inputs)
- **Processing Time**: 7.8 seconds
- **Speed**: 778,230 predictions/second

**Test Results**:
- ✅ Zero negative predictions
- ✅ Zero extreme outliers (>25 kg CO₂)
- ✅ Zero food ordering violations (after correction)
- ✅ 100% accurate impact classification

### Feature Importance Rankings

| Feature | Importance | Interpretation |
|---------|------------|----------------|
| electricity_kwh | 31.09% | Highest impact factor |
| food_type_Non-Veg | 21.71% | Significant dietary impact |
| food_type_Veg | 15.86% | Plant-based diet reduces footprint |
| distance_km | 10.44% | Travel distance matters |
| screen_time_hours | 9.67% | Digital carbon footprint |
| transport_mode_Car | 5.09% | Car vs alternatives |
| transport_mode_Walk | 2.37% | Lowest impact transport |
| food_type_Mixed | 1.90% | Middle ground diet |
| transport_mode_EV | 1.73% | Electric vehicle impact |
| transport_mode_Bus | 0.14% | Public transport efficiency |

## 💡 Usage Example

```python
# Example 1: High Impact Scenario
user_input = {
    'transport_mode': 'Car',
    'distance_km': 50.0,
    'electricity_kwh': 18.0,
    'food_type': 'Non-Veg',
    'screen_time_hours': 10.0
}

# Prediction Result:
Footprint: 11.85 kg CO₂/day
Impact Level: High
Savings Potential: Switch to Bus → Save 1.2 kg CO₂/day

# Example 2: Low Impact Scenario
user_input = {
    'transport_mode': 'Walk',
    'distance_km': 2.0,
    'electricity_kwh': 5.0,
    'food_type': 'Veg',
    'screen_time_hours': 3.0
}

# Prediction Result:
Footprint: 4.32 kg CO₂/day
Impact Level: Low
Tips: "Great job! Maintain your sustainable habits."
```

## 🔧 Technical Specifications

### Impact Classification Thresholds
```python
if footprint < 7.0:
    impact_level = "Low"
elif 7.0 <= footprint <= 9.5:
    impact_level = "Medium"
else:
    impact_level = "High"
```

### Input Validation
- Distance: 0-100 km (step 0.5) = 201 values
- Electricity: 0-20 kWh/day (step 0.5) = 41 values
- Screen Time: 0-24 hours (step 0.5) = 49 values
- Transport: 5 categories
- Food: 3 categories
- **Total Input Space**: 6,057,135 combinations

### Statistical Distribution
- **10th percentile**: 6.25 kg CO₂/day
- **25th percentile**: 7.70 kg CO₂/day
- **Median**: 8.68 kg CO₂/day
- **75th percentile**: 10.46 kg CO₂/day
- **90th percentile**: 11.71 kg CO₂/day

## 🎯 Future Enhancements

- [ ] Add temporal tracking (daily/weekly/monthly trends)
- [ ] Implement user authentication and profile saving
- [ ] Integrate real-time carbon offset recommendations
- [ ] Add social comparison features (anonymized benchmarking)
- [ ] Expand dataset with more diverse behavioral patterns
- [ ] Mobile-responsive design optimization
- [ ] Export reports as PDF/CSV
- [ ] Add gamification elements (achievements, challenges)

## 📝 Known Limitations

1. **R² Score**: Model explains 52.63% of variance - remaining variance due to unmeasured factors
2. **Behavioral Data**: Human behavior has inherent unpredictability
3. **Feature Scope**: Limited to 5 input features - real-world footprints depend on more factors
4. **Dataset Size**: 1,400 records - larger datasets could improve performance

## 📝 License

This project is for educational purposes as part of a Capstone Project.

## 🤝 Contributing

This is a capstone project. Feedback and suggestions are welcome!

---

**Built with Machine Learning, Python, and Streamlit**
**Random Forest | Scikit-learn | Plotly | Kaggle Dataset**
