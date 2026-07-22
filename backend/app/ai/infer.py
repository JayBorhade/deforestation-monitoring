import os
import uuid
import tempfile
import json
from typing import List

import numpy as np
import boto3
import torch
import cv2
from shapely.geometry import Polygon, mapping
import rasterio
from rasterio.transform import Affine

from app.ai.preprocessing import read_raster, normalize_image, resize_image, cloud_mask_stub
from app.ai.model import load_model


def _download_s3(s3_path: str) -> str:
    # s3_path like s3://bucket/key
    parsed = s3_path.replace("s3://", "").split("/", 1)
    if len(parsed) != 2:
        raise ValueError("Invalid s3 path")
    bucket, key = parsed
    client = boto3.client('s3')
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(key)[1])
    os.close(fd)
    client.download_file(bucket, key, tmp)
    return tmp


def _mask_to_polygons(mask: np.ndarray, transform: Affine, min_area_pixels: int = 10):
    """
    Convert binary mask (H,W) to list of polygons in geospatial coordinates using the provided transform.
    """
    contours, _ = cv2.findContours((mask * 255).astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polys = []
    for cnt in contours:
        if len(cnt) < 3:
            continue
        area = cv2.contourArea(cnt)
        if area < min_area_pixels:
            continue
        # cnt is array of points [[x, y]] where x=col, y=row
        coords = []
        for p in cnt.squeeze(axis=1):
            col, row = int(p[0]), int(p[1])
            x, y = rasterio.transform.xy(transform, row, col)
            coords.append((x, y))
        try:
            poly = Polygon(coords)
            if not poly.is_valid:
                poly = poly.buffer(0)
            if poly.area == 0:
                continue
            polys.append(poly)
        except Exception:
            continue
    return polys


def run_inference(input_path: str, threshold: float = 0.5, model_path: str | None = None, device: str = "cpu") -> List[dict]:
    """
    Run inference on a raster input (local path or s3:// path).
    Returns a list of detections: {id, confidence, geometry}
    """
    local_path = input_path
    if input_path.startswith("s3://"):
        local_path = _download_s3(input_path)

    img, transform = read_raster(local_path)  # img H,W,3
    # Keep original size for mapping
    orig_h, orig_w = img.shape[0], img.shape[1]

    # Preprocess
    img_n = normalize_image(img)
    target_size = (256, 256)
    img_rs = resize_image(img_n, target_size)

    # Prepare tensor
    tensor = torch.from_numpy(np.transpose(img_rs, (2, 0, 1))).unsqueeze(0).float()
    tensor = tensor.to(device)

    model = load_model(model_path, device=device)

    with torch.no_grad():
        try:
            out = model(tensor)
            # out shape (1,1,H,W)
            out_np = out.squeeze(0).squeeze(0).cpu().numpy()
        except Exception as e:
            # model failed; fallback to empty detections
            print("Inference failed:", e)
            out_np = np.zeros((target_size[0], target_size[1]), dtype=np.float32)

    # Resize mask back to original image size
    mask_full = cv2.resize(out_np, (orig_w, orig_h), interpolation=cv2.INTER_LINEAR)
    binary = (mask_full >= threshold).astype(np.uint8)

    polygons = _mask_to_polygons(binary, transform, min_area_pixels=20)

    detections = []
    for i, poly in enumerate(polygons):
        det = {
            "id": str(uuid.uuid4()),
            "confidence": float(mask_full.mean()),
            "geometry": mapping(poly)
        }
        detections.append(det)

    # cleanup temp file if downloaded
    if input_path.startswith("s3://"):
        try:
            os.remove(local_path)
        except Exception:
            pass

    return detections
