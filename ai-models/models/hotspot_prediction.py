"""Predictive hotspot detection using historical data."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, List
import json
from pathlib import Path


class HotspotPredictor:
    """ML model for predicting deforestation hotspots."""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1,
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def extract_features(
        self,
        ndvi: np.ndarray,
        elevation: np.ndarray,
        proximity_roads: np.ndarray,
        proximity_settlements: np.ndarray,
        slope: np.ndarray,
    ) -> np.ndarray:
        """Extract features for hotspot prediction."""
        features = []
        
        # Flatten all arrays
        h, w = ndvi.shape
        for i in range(h):
            for j in range(w):
                feature_vector = [
                    ndvi[i, j],
                    elevation[i, j],
                    proximity_roads[i, j],
                    proximity_settlements[i, j],
                    slope[i, j],
                ]
                features.append(feature_vector)
        
        return np.array(features)

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ):
        """Train hotspot predictor model."""
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        print("Hotspot predictor trained successfully")

    def predict(
        self,
        ndvi: np.ndarray,
        elevation: np.ndarray,
        proximity_roads: np.ndarray,
        proximity_settlements: np.ndarray,
        slope: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Predict deforestation hotspots.
        
        Returns:
            - Risk map (H, W) with values 0-1
            - Probabilities (H, W, 2)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call train() first.")
        
        h, w = ndvi.shape
        features = self.extract_features(
            ndvi, elevation, proximity_roads, proximity_settlements, slope
        )
        
        # Scale features
        X_scaled = self.scaler.transform(features)
        
        # Predict
        risk_scores = self.model.predict_proba(X_scaled)[:, 1]
        risk_map = risk_scores.reshape((h, w))
        
        return risk_map

    def save_model(self, path: str):
        """Save model and scaler."""
        import joblib
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, path / "hotspot_model.pkl")
        joblib.dump(self.scaler, path / "scaler.pkl")
        print(f"Model saved to {path}")

    def load_model(self, path: str):
        """Load model and scaler."""
        import joblib
        path = Path(path)
        
        self.model = joblib.load(path / "hotspot_model.pkl")
        self.scaler = joblib.load(path / "scaler.pkl")
        self.is_fitted = True
        print(f"Model loaded from {path}")


class RiskAnalyzer:
    """Analyze and classify risk levels."""

    @staticmethod
    def classify_risk(risk_score: float) -> str:
        """Classify risk score into risk level."""
        if risk_score < 0.25:
            return "low"
        elif risk_score < 0.5:
            return "medium"
        elif risk_score < 0.75:
            return "high"
        else:
            return "critical"

    @staticmethod
    def analyze_risk_map(
        risk_map: np.ndarray,
        threshold: float = 0.5,
    ) -> Dict[str, any]:
        """Analyze risk map and return statistics."""
        high_risk_pixels = np.sum(risk_map >= threshold)
        total_pixels = risk_map.size
        high_risk_percentage = (high_risk_pixels / total_pixels) * 100
        
        return {
            "high_risk_pixels": int(high_risk_pixels),
            "total_pixels": int(total_pixels),
            "high_risk_percentage": float(high_risk_percentage),
            "mean_risk_score": float(risk_map.mean()),
            "max_risk_score": float(risk_map.max()),
            "min_risk_score": float(risk_map.min()),
        }
