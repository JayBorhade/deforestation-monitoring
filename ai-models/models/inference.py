"""Inference pipeline for deforestation detection."""

import torch
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional
from .unet import DeforestationUNet
from .preprocessing import SatelliteImagePreprocessor


class DeforestationInference:
    """Inference engine for deforestation detection."""

    def __init__(
        self,
        model_path: str,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        confidence_threshold: float = 0.5,
    ):
        self.device = device
        self.confidence_threshold = confidence_threshold
        self.preprocessor = SatelliteImagePreprocessor()
        
        # Load model
        self.model = DeforestationUNet(in_channels=4, num_classes=3)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(device)
        self.model.eval()

    def predict_image(
        self, image_path: str
    ) -> Tuple[np.ndarray, Dict[str, float]]:
        """Predict deforestation on a single image.
        
        Returns:
            - Segmentation mask (H, W)
            - Statistics dict
        """
        # Preprocess
        image = self.preprocessor.preprocess(image_path)
        image_tensor = torch.from_numpy(image).float().unsqueeze(0).to(self.device)
        
        # Inference
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = torch.softmax(output, dim=1)
            predictions = torch.argmax(probabilities, dim=1)
        
        # Get predictions and confidence
        pred_mask = predictions.squeeze().cpu().numpy()
        confidence = probabilities.squeeze().cpu().numpy()
        
        # Calculate statistics
        stats = self._calculate_statistics(pred_mask, confidence)
        
        return pred_mask, stats

    def _calculate_statistics(self, mask: np.ndarray, confidence: np.ndarray) -> Dict[str, float]:
        """Calculate deforestation statistics."""
        total_pixels = mask.size
        
        # Class-wise pixel counts
        forest_pixels = np.sum(mask == 0)
        deforestation_pixels = np.sum(mask == 1)
        degradation_pixels = np.sum(mask == 2)
        
        # Percentages
        forest_percentage = (forest_pixels / total_pixels) * 100
        deforestation_percentage = (deforestation_pixels / total_pixels) * 100
        degradation_percentage = (degradation_pixels / total_pixels) * 100
        
        # Average confidence per class
        forest_conf = confidence[0].mean() if forest_pixels > 0 else 0.0
        deforestation_conf = confidence[1].mean() if deforestation_pixels > 0 else 0.0
        degradation_conf = confidence[2].mean() if degradation_pixels > 0 else 0.0
        
        return {
            "forest_percentage": float(forest_percentage),
            "deforestation_percentage": float(deforestation_percentage),
            "degradation_percentage": float(degradation_percentage),
            "forest_confidence": float(forest_conf),
            "deforestation_confidence": float(deforestation_conf),
            "degradation_confidence": float(degradation_conf),
            "total_pixels": int(total_pixels),
            "deforestation_pixels": int(deforestation_pixels),
            "degradation_pixels": int(degradation_pixels),
        }

    def predict_batch(
        self, image_paths: list
    ) -> Tuple[list, list]:
        """Predict on multiple images."""
        masks = []
        stats = []
        
        for image_path in image_paths:
            try:
                mask, stat = self.predict_image(image_path)
                masks.append(mask)
                stats.append(stat)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        
        return masks, stats

    def save_prediction(self, mask: np.ndarray, output_path: str):
        """Save prediction mask to file."""
        np.save(output_path, mask)
        print(f"Mask saved to {output_path}")

    def save_visualization(
        self,
        image_path: str,
        mask: np.ndarray,
        output_path: str,
    ):
        """Save visualization of prediction."""
        import cv2
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (mask.shape[1], mask.shape[0]))
        
        # Create color map
        color_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
        color_mask[mask == 0] = [0, 255, 0]  # Green for forest
        color_mask[mask == 1] = [255, 0, 0]  # Red for deforestation
        color_mask[mask == 2] = [255, 165, 0]  # Orange for degradation
        
        # Blend
        visualization = cv2.addWeighted(image, 0.5, color_mask, 0.5, 0)
        
        # Save
        visualization_bgr = cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, visualization_bgr)
        print(f"Visualization saved to {output_path}")
