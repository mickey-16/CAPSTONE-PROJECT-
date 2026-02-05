"""
Three-Tier Tip Generation Engine
Level 1: Rule-Based Tips
Level 2: What-If Analysis
Level 3: Feature Importance Analysis
"""
import pandas as pd
from typing import Dict, List, Tuple


class TipGenerator:
    def __init__(self, model, data_loader):
        self.model = model
        self.data_loader = data_loader
        
        # Tip database organized by category
        self.tip_database = {
            'transport_mode': {
                'Car': "🚗 Consider carpooling or switching to Bus or EV to reduce emissions significantly.",
                'Bus': "🚌 Great choice! Public transport is eco-friendly. Keep it up!",
                'Bike': "🚴 Biking is carbon-neutral and healthy. Excellent choice!",
                'EV': "⚡ Electric vehicles are excellent! Clean and efficient transportation.",
                'Walk': "🚶 Walking is the best for the environment! You're doing great!"
            },
            'electricity': {
                'high': "💡 Your electricity usage is high. Try LED bulbs, unplug devices, and use energy-efficient appliances.",
                'medium': "⚡ Consider reducing electricity usage with smart plugs and energy-efficient devices.",
                'low': "✅ Your electricity usage is well-managed. Keep up the good work!"
            },
            'food': {
                'Non-Veg': "🍖 Meat production has high carbon emissions. Try 'Meatless Mondays' or switch to Mixed diet.",
                'Mixed': "🥗 Good choice! Balanced diets have moderate emissions. Consider more plant-based meals.",
                'Veg': "🌱 Plant-based diets have the lowest carbon footprint. You're making a great impact!"
            },
            'screen_time': {
                'high': "📱 High screen time increases electricity use. Try digital detox or screen-free hours.",
                'medium': "⏰ Moderate screen time. Consider reducing it to save energy and improve well-being.",
                'low': "✅ Your screen time is well-balanced. Great job!"
            },
            'distance': {
                'high': "🛣️ Long distances traveled increase emissions. Consider remote work or relocating closer.",
                'medium': "🚗 Try to consolidate trips or use eco-friendly transport for longer distances.",
                'low': "✅ Your travel distance is minimal. Keep it up!"
            }
        }
        
        # Alternative options for what-if analysis
        self.alternatives = {
            'transport_mode': {
                'Car': ['Bus', 'EV', 'Bike'],
                'Bus': ['Bike', 'Walk'],
                'EV': ['Bus', 'Bike'],
                'Bike': [],
                'Walk': []
            },
            'food_type': {
                'Non-Veg': ['Mixed', 'Veg'],
                'Mixed': ['Veg'],
                'Veg': []
            }
        }
    
    # ==================== LEVEL 1: RULE-BASED TIPS ====================
    
    def generate_rule_based_tips(self, user_input: Dict) -> List[str]:
        """
        Level 1: Generate tips based on simple if/else rules
        """
        tips = []
        
        # Transport mode tip
        transport = user_input.get('transport_mode', '')
        if transport in self.tip_database['transport_mode']:
            tips.append(self.tip_database['transport_mode'][transport])
        
        # Electricity usage tip
        electricity = user_input.get('electricity_kwh', 0)
        if electricity > 10:
            tips.append(self.tip_database['electricity']['high'])
        elif electricity > 6:
            tips.append(self.tip_database['electricity']['medium'])
        else:
            tips.append(self.tip_database['electricity']['low'])
        
        # Food type tip
        food = user_input.get('food_type', '')
        if food in self.tip_database['food']:
            tips.append(self.tip_database['food'][food])
        
        # Screen time tip
        screen_time = user_input.get('screen_time_hours', 0)
        if screen_time > 8:
            tips.append(self.tip_database['screen_time']['high'])
        elif screen_time > 4:
            tips.append(self.tip_database['screen_time']['medium'])
        else:
            tips.append(self.tip_database['screen_time']['low'])
        
        # Distance tip
        distance = user_input.get('distance_km', 0)
        if distance > 50:
            tips.append(self.tip_database['distance']['high'])
        elif distance > 20:
            tips.append(self.tip_database['distance']['medium'])
        else:
            tips.append(self.tip_database['distance']['low'])
        
        return tips
    
    # ==================== LEVEL 2: WHAT-IF ANALYSIS ====================
    
    def generate_what_if_tips(self, user_input: Dict, baseline_footprint: float) -> List[Dict]:
        """
        Level 2: Run simulations with alternative choices
        """
        what_if_results = []
        
        # Test transport alternatives
        if user_input['transport_mode'] in self.alternatives['transport_mode']:
            for alt_transport in self.alternatives['transport_mode'][user_input['transport_mode']]:
                # Create alternative input
                alt_input = user_input.copy()
                alt_input['transport_mode'] = alt_transport
                
                # Predict with alternative
                X_alt = self.data_loader.preprocess_user_input(alt_input)
                alt_footprint = self.model.predict_footprint(X_alt)
                
                savings = baseline_footprint - alt_footprint
                
                if savings > 0.5:  # Only show if meaningful savings
                    what_if_results.append({
                        'category': 'transport',
                        'change': f"Switch from {user_input['transport_mode']} to {alt_transport}",
                        'savings': savings,
                        'new_footprint': alt_footprint,
                        'icon': '🚗➡️🚌'
                    })
        
        # Test food alternatives
        if user_input['food_type'] in self.alternatives['food_type']:
            for alt_food in self.alternatives['food_type'][user_input['food_type']]:
                alt_input = user_input.copy()
                alt_input['food_type'] = alt_food
                
                X_alt = self.data_loader.preprocess_user_input(alt_input)
                alt_footprint = self.model.predict_footprint(X_alt)
                
                savings = baseline_footprint - alt_footprint
                
                if savings > 0.5:
                    what_if_results.append({
                        'category': 'food',
                        'change': f"Switch from {user_input['food_type']} to {alt_food} diet",
                        'savings': savings,
                        'new_footprint': alt_footprint,
                        'icon': '🍖➡️🥗'
                    })
        
        # Test reducing screen time by 50%
        if user_input['screen_time_hours'] > 4:
            alt_input = user_input.copy()
            alt_input['screen_time_hours'] = user_input['screen_time_hours'] * 0.5
            
            X_alt = self.data_loader.preprocess_user_input(alt_input)
            alt_footprint = self.model.predict_footprint(X_alt)
            
            savings = baseline_footprint - alt_footprint
            
            if savings > 0.5:
                what_if_results.append({
                    'category': 'screen_time',
                    'change': f"Reduce screen time by 50%",
                    'savings': savings,
                    'new_footprint': alt_footprint,
                    'icon': '📱➡️📵'
                })
        
        # Sort by savings (highest first)
        what_if_results.sort(key=lambda x: x['savings'], reverse=True)
        
        return what_if_results
    
    # ==================== LEVEL 3: FEATURE IMPORTANCE ====================
    
    def generate_feature_importance_tips(self, user_input: Dict, X_preprocessed) -> List[Dict]:
        """
        Level 3: Identify top contributing factors using feature importance
        """
        # Get top contributing factors for this specific input
        top_factors = self.model.get_top_contributing_factors(X_preprocessed, top_n=3)
        
        tips = []
        for feature, contribution in top_factors:
            # Map feature to category and generate tip
            category = self._map_feature_to_category(feature)
            tip = self._get_category_tip(category, user_input)
            
            if tip:
                tips.append({
                    'feature': feature,
                    'contribution': contribution,
                    'category': category,
                    'tip': tip
                })
        
        return tips
    
    def _map_feature_to_category(self, feature: str) -> str:
        """Map one-hot encoded feature to original category"""
        if 'transport_mode' in feature:
            return 'transport'
        elif 'food_type' in feature:
            return 'food'
        elif 'electricity' in feature:
            return 'electricity'
        elif 'screen_time' in feature:
            return 'screen_time'
        elif 'distance' in feature:
            return 'distance'
        return 'general'
    
    def _get_category_tip(self, category: str, user_input: Dict) -> str:
        """Get specific tip for a category based on user input"""
        if category == 'transport':
            transport = user_input.get('transport_mode', '')
            return self.tip_database['transport_mode'].get(transport, '')
        
        elif category == 'electricity':
            electricity = user_input.get('electricity_kwh', 0)
            if electricity > 10:
                return self.tip_database['electricity']['high']
            elif electricity > 6:
                return self.tip_database['electricity']['medium']
            return self.tip_database['electricity']['low']
        
        elif category == 'food':
            food = user_input.get('food_type', '')
            return self.tip_database['food'].get(food, '')
        
        elif category == 'screen_time':
            screen_time = user_input.get('screen_time_hours', 0)
            if screen_time > 8:
                return self.tip_database['screen_time']['high']
            elif screen_time > 4:
                return self.tip_database['screen_time']['medium']
            return self.tip_database['screen_time']['low']
        
        elif category == 'distance':
            distance = user_input.get('distance_km', 0)
            if distance > 50:
                return self.tip_database['distance']['high']
            elif distance > 20:
                return self.tip_database['distance']['medium']
            return self.tip_database['distance']['low']
        
        return ""
    
    # ==================== UNIFIED TIP GENERATION ====================
    
    def generate_all_tips(self, user_input: Dict, baseline_footprint: float, X_preprocessed):
        """Generate all three levels of tips"""
        return {
            'level_1_rules': self.generate_rule_based_tips(user_input),
            'level_2_what_if': self.generate_what_if_tips(user_input, baseline_footprint),
            'level_3_importance': self.generate_feature_importance_tips(user_input, X_preprocessed)
        }
