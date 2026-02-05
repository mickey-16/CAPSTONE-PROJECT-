# 🌍 Carbon Footprint Prediction System

A machine learning-powered web application that predicts personal carbon footprints and provides intelligent, personalized tips to reduce environmental impact.

## 🎯 Features

### Dual-Output ML System
- **Random Forest Regression**: Predicts exact carbon footprint values (kg CO₂)
- **Rule-Based Classification**: Categorizes impact levels (High/Medium/Low)

### Three-Tier Tip Generation Engine

#### Level 1: Rule-Based Tips
Simple, actionable advice based on user inputs using if/else logic.

#### Level 2: What-If Analysis
Intelligent simulations showing potential CO₂ savings by making specific lifestyle changes:
- Switch transport modes
- Change diet types
- Increase renewable energy usage
- Reduce screen time

#### Level 3: Feature Importance Analysis
ML-powered insights identifying which factors contribute most to your carbon footprint.

### Interactive Web Interface
Built with Streamlit featuring:
- 📊 Real-time carbon footprint visualization
- 🎨 Interactive gauge charts and graphs
- 💡 Personalized action plans
- 🔄 What-if scenario comparisons

## 📋 Dataset

Source: [Kaggle - Personal Carbon Footprint Behavior Dataset](https://www.kaggle.com/datasets/sonalshinde123/personal-carbon-footprint-behavior-dataset)

**Input Features:**
- `transport_mode`: Car, Motorbike, Public Transport, EV, Walk, Bicycle
- `distance_km`: Daily travel distance
- `electricity_kwh`: Monthly electricity usage
- `renewable_usage_pct`: Percentage of renewable energy used
- `food_type`: Meat, Vegetarian, Vegan, Pescatarian
- `screen_time_hours`: Daily screen time

**Target Variables:**
- `carbon_footprint_kg`: Carbon footprint value (regression)
- `carbon_impact_level`: High/Medium/Low (classification)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Download the dataset from Kaggle
- Preprocess and clean the data
- Train the Random Forest model
- Save the model to `models/carbon_footprint_model.pkl`

### 3. Run the Web Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Capestone project/
│
├── app.py                      # Streamlit web application
├── train_model.py              # ML model training script
├── data_loader.py              # Data loading and preprocessing
├── tip_generator.py            # Three-tier tip generation engine
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── models/                     # Saved models (created after training)
│   ├── carbon_footprint_model.pkl
│   └── preprocessor.pkl
│
└── load_dataset.py            # Utility script for dataset exploration
```

## 🎓 How It Works

### 1. Data Preprocessing
- Removes unnecessary columns (`user_id`, `day_type`, `waste_generated_kg`, `eco_actions`)
- Applies one-hot encoding to categorical features (`transport_mode`, `food_type`)
- Scales numerical features for optimal model performance

### 2. Model Training
- **Algorithm**: Random Forest Regressor
- **Parameters**: 100 trees, max depth 15
- **Performance**: R² score ~0.85+, low RMSE

### 3. Prediction Flow
```
User Input → Preprocessing → Model Prediction → Impact Classification → Tip Generation
```

### 4. Tip Generation

**Level 1 - Rule-Based:**
```python
IF transport_mode == 'Car' AND distance > 20:
    SUGGEST "Consider carpooling or public transport"
```

**Level 2 - What-If:**
```python
Baseline: Car → 450 kg CO₂
Alternative: Public Transport → 380 kg CO₂
Tip: "Switch to save 70 kg CO₂ per day!"
```

**Level 3 - Feature Importance:**
```python
Model identifies: electricity_kwh contributes 60%
Tip: "Your electricity usage is the biggest factor. Try LED bulbs."
```

## 📊 Model Performance

- **R² Score**: ~0.85-0.90
- **RMSE**: ~1.5-2.0 kg CO₂
- **MAE**: ~1.0-1.5 kg CO₂

Top Contributing Features:
1. Electricity usage (kWh)
2. Transport mode (Car vs others)
3. Renewable energy percentage
4. Food type (Meat vs plant-based)

## 💡 Usage Example

```python
# Example prediction
user_input = {
    'transport_mode': 'Car',
    'distance_km': 25.0,
    'electricity_kwh': 300.0,
    'renewable_usage_pct': 20,
    'food_type': 'Meat',
    'screen_time_hours': 8.0
}

# Result
Footprint: 12.5 kg CO₂/day
Impact Level: High
Top Tip: "Switch to Public Transport to save 4.2 kg CO₂/day"
```

## 🎯 Future Enhancements

- [ ] Add more input features (waste, water usage)
- [ ] Integrate real-time data sources
- [ ] Mobile app version
- [ ] Social comparison features
- [ ] Carbon offset recommendations
- [ ] Historical tracking dashboard

## 📝 License

This project is for educational purposes as part of a Capstone Project.

## 🤝 Contributing

This is a capstone project, but suggestions and feedback are welcome!

## 📧 Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Built with ❤️ using Machine Learning, Python, and Streamlit**
