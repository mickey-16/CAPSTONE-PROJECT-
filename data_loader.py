"""
Data loader and preprocessor for carbon footprint dataset
"""
import pandas as pd
import kagglehub
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

class CarbonFootprintDataLoader:
    def __init__(self):
        self.label_encoders = {}
        self.feature_columns = None
        self.categorical_columns = ['transport_mode', 'food_type']
        self.numerical_columns = ['distance_km', 'electricity_kwh', 'screen_time_hours']
        
    def load_raw_data(self):
        """Load dataset from Kaggle"""
        print("Downloading dataset from Kaggle...")
        dataset_path = kagglehub.dataset_download("sonalshinde123/personal-carbon-footprint-behavior-dataset")
        csv_file = os.path.join(dataset_path, "personal_carbon_footprint_behavior.csv")
        
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} records")
        return df
    
    def preprocess_data(self, df, fit_encoders=True):
        """
        Remove unnecessary columns and preprocess data
        
        Columns to remove: user_id, day_type, waste_generated_kg, eco_actions, renewable_usage_pct
        Columns to keep: transport_mode, distance_km, electricity_kwh, 
                        food_type, screen_time_hours,
                        carbon_footprint_kg, carbon_impact_level
        """
        # Remove unnecessary columns
        columns_to_remove = ['user_id', 'day_type', 'waste_generated_kg', 'eco_actions', 'renewable_usage_pct']
        df_cleaned = df.drop(columns=columns_to_remove, errors='ignore')
        
        # Separate features and targets
        X = df_cleaned.drop(columns=['carbon_footprint_kg', 'carbon_impact_level'])
        y_regression = df_cleaned['carbon_footprint_kg']
        y_classification = df_cleaned['carbon_impact_level']
        
        # Apply one-hot encoding to categorical columns
        X_encoded = pd.get_dummies(X, columns=self.categorical_columns, drop_first=False)
        
        # Store feature column names
        if fit_encoders:
            self.feature_columns = X_encoded.columns.tolist()
        
        print(f"✓ Preprocessed data: {X_encoded.shape[1]} features")
        return X_encoded, y_regression, y_classification
    
    def prepare_training_data(self, test_size=0.2, random_state=42):
        """Load and split data for training"""
        # Load raw data
        df = self.load_raw_data()
        
        # Preprocess
        X, y_regression, y_classification = self.preprocess_data(df, fit_encoders=True)
        
        # Split data
        X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf = train_test_split(
            X, y_regression, y_classification, 
            test_size=test_size, 
            random_state=random_state
        )
        
        print(f"✓ Training set: {len(X_train)} samples")
        print(f"✓ Test set: {len(X_test)} samples")
        
        return X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf
    
    def preprocess_user_input(self, input_data):
        """
        Preprocess user input for prediction
        
        Args:
            input_data: dict with keys matching feature names
        
        Returns:
            DataFrame ready for model prediction
        """
        # Create DataFrame from input
        df = pd.DataFrame([input_data])
        
        # Apply one-hot encoding
        df_encoded = pd.get_dummies(df, columns=self.categorical_columns, drop_first=False)
        
        # Ensure all feature columns are present (add missing columns with 0)
        for col in self.feature_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        # Reorder columns to match training data
        df_encoded = df_encoded[self.feature_columns]
        
        return df_encoded
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Save preprocessor configuration"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        config = {
            'feature_columns': self.feature_columns,
            'categorical_columns': self.categorical_columns,
            'numerical_columns': self.numerical_columns
        }
        with open(filepath, 'wb') as f:
            pickle.dump(config, f)
        print(f"✓ Saved preprocessor to {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Load preprocessor configuration"""
        with open(filepath, 'rb') as f:
            config = pickle.load(f)
        self.feature_columns = config['feature_columns']
        self.categorical_columns = config['categorical_columns']
        self.numerical_columns = config['numerical_columns']
        print(f"✓ Loaded preprocessor from {filepath}")


if __name__ == "__main__":
    # Test the data loader
    loader = CarbonFootprintDataLoader()
    X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf = loader.prepare_training_data()
    
    print("\nFeature columns:")
    print(loader.feature_columns)
    
    print("\nSample data:")
    print(X_train.head())
