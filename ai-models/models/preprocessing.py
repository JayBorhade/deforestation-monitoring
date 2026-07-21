"""Preprocessing utilities for satellite imagery."""

import numpy as np
import cv2
from typing import Tuple, Optional
from pathlib import Path


class SatelliteImagePreprocessor:
    """Preprocessing pipeline for satellite images."""

    def __init__(
        self,
        target_size: Tuple[int, int] = (256, 256),
        normalize: bool = True,
        augment: bool = False,
    ):
        self.target_size = target_size
        self.normalize = normalize
        self.augment = augment
        
        # Sentinel-2 band statistics (approximate)
        self.mean = np.array([0.485, 0.456, 0.406])
        self.std = np.array([0.229, 0.224, 0.225])

    def load_image(self, image_path: str) -> np.ndarray:
        """Load image from file."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def resize(self, image: np.ndarray) -> np.ndarray:
        """Resize image to target size."""
        return cv2.resize(image, self.target_size, interpolation=cv2.INTER_AREA)

    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize image using ImageNet statistics."""
        if image.dtype != np.float32:
            image = image.astype(np.float32) / 255.0
        
        # Normalize each channel
        for i in range(min(3, image.shape[2])):
            image[:, :, i] = (image[:, :, i] - self.mean[i]) / self.std[i]
        
        return image

    def calculate_indices(self, image: np.ndarray) -> dict:
        """Calculate vegetation and water indices.
        
        NDVI: Normalized Difference Vegetation Index
        NDBI: Normalized Difference Built-up Index
        NDWI: Normalized Difference Water Index
        """
        indices = {}
        
        # Assuming image has at least 4 channels (RGB + NIR)
        if image.shape[2] >= 4:
            red = image[:, :, 0].astype(np.float32)
            nir = image[:, :, 3].astype(np.float32)
            
            # NDVI
            ndvi = (nir - red) / (nir + red + 1e-8)
            indices['ndvi'] = ndvi
        
        return indices

    def apply_clahe(self, image: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
        """Apply Contrast Limited Adaptive Histogram Equalization."""
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        
        # Apply to each channel
        enhanced = np.zeros_like(image)
        for i in range(image.shape[2]):
            enhanced[:, :, i] = clahe.apply((image[:, :, i] * 255).astype(np.uint8))
        
        return enhanced.astype(np.float32) / 255.0

    def augment_image(self, image: np.ndarray) -> np.ndarray:
        """Apply data augmentation."""
        if not self.augment:
            return image
        
        # Random rotation
        if np.random.rand() > 0.5:
            angle = np.random.randint(-15, 15)
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
            image = cv2.warpAffine(image, M, (w, h))
        
        # Random flip
        if np.random.rand() > 0.5:
            image = cv2.flip(image, 1)
        
        # Random brightness adjustment
        if np.random.rand() > 0.5:
            brightness = np.random.uniform(0.8, 1.2)
            image = np.clip(image * brightness, 0, 1)
        
        return image

    def preprocess(self, image_path: str, augment: bool = False) -> np.ndarray:
        """Full preprocessing pipeline."""
        # Load image
        image = self.load_image(image_path)
        
        # Resize
        image = self.resize(image)
        
        # Calculate indices
        indices = self.calculate_indices(image)
        
        # Augmentation
        if augment:
            image = self.augment_image(image)
        
        # Normalize
        if self.normalize:
            image = self.normalize_image(image)
        
        # Convert to tensor format (C, H, W)
        image = np.transpose(image, (2, 0, 1))
        
        return image


class MaskProcessor:
    """Processor for segmentation masks."""

    def __init__(self, target_size: Tuple[int, int] = (256, 256)):
        self.target_size = target_size

    def load_mask(self, mask_path: str) -> np.ndarray:
        """Load mask from file."""
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise ValueError(f"Failed to load mask: {mask_path}")
        return mask

    def resize_mask(self, mask: np.ndarray) -> np.ndarray:
        """Resize mask to target size using nearest neighbor."""
        return cv2.resize(mask, self.target_size, interpolation=cv2.INTER_NEAREST)

    def normalize_mask(self, mask: np.ndarray) -> np.ndarray:
        """Normalize mask to [0, 1] range."""
        mask_max = mask.max()
        if mask_max > 0:
            mask = mask.astype(np.float32) / mask_max
        return mask

    def process(self, mask_path: str) -> np.ndarray:
        """Full mask processing pipeline."""
        mask = self.load_mask(mask_path)
        mask = self.resize_mask(mask)
        mask = self.normalize_mask(mask)
        return mask
