"""
ML Model Training Script for Carbon Footprint Prediction
Uses Random Forest Regression + Rule-based Classification
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os
from data_loader import CarbonFootprintDataLoader


class CarbonFootprintModel:
    def __init__(self):
        self.regression_model = None
        self.feature_importance = None
        self.feature_names = None
        
    def train_regression_model(self, X_train, y_train, n_estimators=150, random_state=42):
        """Train Random Forest Regression model for carbon_footprint_kg"""
        print("Training Random Forest Regression model...")
        
        self.regression_model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=12,
            min_samples_split=10,
            min_samples_leaf=4,
            max_features='sqrt',
            random_state=random_state,
            n_jobs=-1
        )
        
        self.regression_model.fit(X_train, y_train)
        self.feature_names = X_train.columns.tolist()
        self.feature_importance = dict(zip(
            self.feature_names,
            self.regression_model.feature_importances_
        ))
        
        print("✓ Model trained successfully")
        return self.regression_model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate regression model performance"""
        predictions = self.regression_model.predict(X_test)
        
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        print("\n" + "="*60)
        print("MODEL EVALUATION METRICS")
        print("="*60)
        print(f"R² Score:                 {r2:.4f}")
        print(f"Root Mean Squared Error:  {rmse:.4f} kg CO2")
        print(f"Mean Absolute Error:      {mae:.4f} kg CO2")
        print("="*60)
        
        return {
            'r2': r2,
            'rmse': rmse,
            'mae': mae,
            'predictions': predictions
        }
    
    def predict_footprint(self, X):
        """Predict carbon footprint value"""
        if self.regression_model is None:
            raise ValueError("Model not trained. Call train_regression_model first.")
        
        prediction = self.regression_model.predict(X)[0]
        return prediction
    
    def predict_footprint_corrected(self, X, food_type=None):
        """
        Predict carbon footprint with food ordering correction
        Ensures: Non-Veg >= Mixed >= Veg for same other inputs
        """
        if self.regression_model is None:
            raise ValueError("Model not trained. Call train_regression_model first.")
        
        prediction = self.regression_model.predict(X)[0]
        
        # If food_type provided, apply correction
        if food_type is not None:
            # Get predictions for all food types with same other inputs
            X_df = X.copy()
            
            # Reset food type columns
            food_cols = [col for col in X_df.columns if col.startswith('food_type_')]
            for col in food_cols:
                X_df[col] = 0
            
            # Get predictions for each food type
            preds = {}
            for food in ['Non-Veg', 'Mixed', 'Veg']:
                X_temp = X_df.copy()
                X_temp[f'food_type_{food}'] = 1
                preds[food] = self.regression_model.predict(X_temp)[0]
            
            # Apply ordering correction: ensure Non-Veg >= Mixed >= Veg
            if preds['Mixed'] > preds['Non-Veg']:
                preds['Mixed'] = preds['Non-Veg']
            if preds['Veg'] > preds['Mixed']:
                preds['Veg'] = preds['Mixed']
            
            # Return corrected prediction for requested food type
            prediction = preds[food_type]
        
        return prediction
    
    def classify_impact_level(self, carbon_footprint_kg):
        """
        Rule-based classification for carbon_impact_level
        More efficient than training a separate classifier
        
        Rules based on data distribution:
        - Low: < 7 kg CO2 (below median)
        - Medium: 7-9.5 kg CO2 (median to 70th percentile)
        - High: > 9.5 kg CO2 (above 70th percentile)
        """
        if carbon_footprint_kg > 9.5:
            return "High"
        elif carbon_footprint_kg >= 7:
            return "Medium"
        else:
            return "Low"
    
    def get_feature_importance(self, top_n=None):
        """Get feature importance rankings"""
        if self.feature_importance is None:
            raise ValueError("Model not trained yet.")
        
        # Sort by importance
        sorted_importance = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        if top_n:
            sorted_importance = sorted_importance[:top_n]
        
        return sorted_importance
    
    def get_top_contributing_factors(self, X_input, top_n=3):
        """
        Identify which input features contribute most to the prediction
        for a specific user input
        """
        if self.regression_model is None:
            raise ValueError("Model not trained.")
        
        # Get feature values
        feature_values = X_input.iloc[0].to_dict()
        
        # Calculate contribution (feature_value * feature_importance)
        contributions = {}
        for feature, value in feature_values.items():
            if value > 0:  # Only consider active features
                importance = self.feature_importance.get(feature, 0)
                contributions[feature] = value * importance
        
        # Sort by contribution
        sorted_contributions = sorted(
            contributions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        return sorted_contributions
    
    def save_model(self, filepath='models/carbon_footprint_model.pkl'):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'regression_model': self.regression_model,
            'feature_importance': self.feature_importance,
            'feature_names': self.feature_names
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to {filepath}")
    
    def load_model(self, filepath='models/carbon_footprint_model.pkl'):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.regression_model = model_data['regression_model']
        self.feature_importance = model_data['feature_importance']
        self.feature_names = model_data['feature_names']
        
        print(f"✓ Model loaded from {filepath}")


def train_and_save_model():
    """Main training pipeline"""
    print("="*60)
    print("CARBON FOOTPRINT ML MODEL TRAINING")
    print("="*60)
    
    # Load and prepare data
    loader = CarbonFootprintDataLoader()
    X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf = loader.prepare_training_data()
    
    # Train model
    model = CarbonFootprintModel()
    model.train_regression_model(X_train, y_train_reg)
    
    # Evaluate model
    metrics = model.evaluate_model(X_test, y_test_reg)
    
    # Show feature importance
    print("\nTOP 10 MOST IMPORTANT FEATURES:")
    print("="*60)
    for i, (feature, importance) in enumerate(model.get_feature_importance(top_n=10), 1):
        print(f"{i:2d}. {feature:30s} {importance:.4f}")
    print("="*60)
    
    # Save model and preprocessor
    model.save_model()
    loader.save_preprocessor()
    
    print("\n✓ Training complete! Model ready for predictions.")
    
    return model, loader, metrics


if __name__ == "__main__":
    train_and_save_model()
