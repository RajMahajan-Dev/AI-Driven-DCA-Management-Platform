import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Tuple


class RecoveryScorePredictor:
    """
    AI/ML model for predicting debt recovery probability.
    
    Uses Logistic Regression to predict recovery score (0-1) based on:
    - Overdue amount
    - Ageing days
    
    This is a baseline model for the hackathon. In production, this would:
    - Use more features (customer history, payment patterns, etc.)
    - Be trained on historical data
    - Be regularly retrained and validated
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.scaler = None
        self.model_path = model_path
        
        # Try to load existing model
        if model_path and os.path.exists(model_path):
            self.load_model()
        else:
            # Initialize with a baseline model
            self.initialize_baseline_model()
    
    def initialize_baseline_model(self):
        """
        Initialize a baseline logistic regression model.
        
        Training data is synthetic for demonstration purposes.
        In production, this would be trained on actual historical recovery data.
        """
        # Synthetic training data
        # Features: [overdue_amount, ageing_days]
        # Label: 1 (recovered), 0 (not recovered)
        
        # Lower amounts and ageing tend to have better recovery
        X_train = np.array([
            [5000, 15],    # Small amount, recent -> likely recover
            [10000, 30],   # Medium amount, medium age -> likely recover
            [15000, 25],   # Medium amount, recent -> likely recover
            [8000, 45],    # Small-medium amount, older -> moderate
            [25000, 60],   # High amount, old -> moderate
            [50000, 90],   # Very high, very old -> unlikely
            [60000, 120],  # Very high, very old -> unlikely
            [45000, 100],  # High amount, very old -> unlikely
            [7000, 20],    # Small amount, recent -> likely
            [12000, 35],   # Medium amount -> moderate
            [20000, 70],   # High amount, old -> moderate
            [55000, 95],   # Very high, very old -> unlikely
            [3000, 10],    # Very small, very recent -> very likely
            [35000, 80],   # High, old -> unlikely
            [18000, 50],   # Medium-high, medium-old -> moderate
        ])
        
        y_train = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0])
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train logistic regression
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_train_scaled, y_train)
    
    def predict_recovery_score(self, overdue_amount: float, ageing_days: int) -> float:
        """
        Predict recovery probability score.
        
        Args:
            overdue_amount: Amount overdue in currency
            ageing_days: Number of days the debt is overdue
        
        Returns:
            Recovery probability score between 0 and 1
        """
        if self.model is None or self.scaler is None:
            # Fallback to deterministic scoring if model not available
            return self._deterministic_score(overdue_amount, ageing_days)
        
        # Prepare input
        X = np.array([[overdue_amount, ageing_days]])
        X_scaled = self.scaler.transform(X)
        
        # Predict probability
        probability = self.model.predict_proba(X_scaled)[0][1]  # Probability of class 1 (recovery)
        
        return round(float(probability), 4)
    
    def _deterministic_score(self, overdue_amount: float, ageing_days: int) -> float:
        """
        Fallback deterministic scoring logic.
        
        Score decreases with:
        - Higher overdue amount
        - More ageing days
        """
        # Normalize amount (assume max 100k)
        amount_factor = max(0, 1 - (overdue_amount / 100000))
        
        # Normalize ageing (assume max 180 days)
        ageing_factor = max(0, 1 - (ageing_days / 180))
        
        # Weighted combination (ageing is slightly more important)
        score = (amount_factor * 0.4) + (ageing_factor * 0.6)
        
        return round(score, 4)
    
    def save_model(self):
        """Save model and scaler to disk."""
        if self.model_path and self.model and self.scaler:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, self.model_path)
    
    def load_model(self):
        """Load model and scaler from disk."""
        if self.model_path and os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
    
    def get_model_info(self) -> dict:
        """Get information about the model."""
        return {
            "model_type": "Logistic Regression",
            "features": ["overdue_amount", "ageing_days"],
            "output": "Recovery probability score (0-1)",
            "status": "baseline" if self.model else "fallback",
            "description": "Predicts likelihood of debt recovery based on amount and ageing"
        }


# Singleton instance
_predictor = None


def get_predictor() -> RecoveryScorePredictor:
    """Get singleton instance of the predictor."""
    global _predictor
    if _predictor is None:
        _predictor = RecoveryScorePredictor()
    return _predictor
