import os
import tempfile
from typing import Tuple

import rasterio
import numpy as np
import cv2


def read_raster(path: str):
    """
    Read a raster file and return an RGB numpy array (H, W, C) and the affine transform.
    Supports local file paths. S3 handled by caller (download first).
    """
    with rasterio.open(path) as src:
        # Try to read first 3 bands (RGB). If fewer bands, replicate or trim as needed.
        count = src.count
        bands_to_read = min(3, count)
        arr = src.read(list(range(1, bands_to_read + 1)))  # (C, H, W)
        arr = np.transpose(arr, (1, 2, 0))  # (H, W, C)
        transform = src.transform
    # If only 1 band, stack to 3
    if arr.shape[2] == 1:
        arr = np.repeat(arr, 3, axis=2)
    # If 2 bands, add a zero band
    if arr.shape[2] == 2:
        arr = np.concatenate([arr, np.zeros((arr.shape[0], arr.shape[1], 1), dtype=arr.dtype)], axis=2)
    return arr, transform


def normalize_image(img: np.ndarray) -> np.ndarray:
    """Convert image to float32 and normalize to [0,1]."""
    img = img.astype(np.float32)
    # Simple min-max per-channel normalization
    for c in range(img.shape[2]):
        ch = img[:, :, c]
        minv = ch.min()
        maxv = ch.max()
        if maxv > minv:
            img[:, :, c] = (ch - minv) / (maxv - minv)
        else:
            img[:, :, c] = 0.0
    return img


def resize_image(img: np.ndarray, target_size: Tuple[int, int]):
    """Resize image to target_size (H, W) using bilinear interpolation."""
    h, w = target_size
    resized = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
    return resized


def cloud_mask_stub(img: np.ndarray) -> np.ndarray:
    """
    A very conservative cloud mask stub: returns zeros (no-cloud) for now.
    Replace with real cloud detection later.
    """
    return np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
