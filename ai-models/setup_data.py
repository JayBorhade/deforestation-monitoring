"""Script to download and prepare sample satellite data."""

import os
import sys
from pathlib import Path


def setup_directories():
    """Create necessary directories."""
    directories = [
        "datasets/train/images",
        "datasets/train/masks",
        "datasets/val/images",
        "datasets/val/masks",
        "datasets/test/images",
        "models",
        "checkpoints",
        "predictions",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")


def create_sample_data():
    """Create sample synthetic data for testing."""
    import numpy as np
    
    print("\n📊 Creating sample data...")
    
    # Create sample training data
    num_samples = 10
    for i in range(num_samples):
        # Create random image (4 channels: RGB + NIR)
        image = np.random.rand(256, 256, 4).astype(np.float32)
        mask = np.random.randint(0, 3, (256, 256), dtype=np.int32)
        
        image_path = f"datasets/train/images/sample_{i:04d}.npy"
        mask_path = f"datasets/train/masks/sample_{i:04d}.npy"
        
        np.save(image_path, image)
        np.save(mask_path, mask)
    
    print(f"✓ Created {num_samples} training samples")
    
    # Create sample validation data
    for i in range(5):
        image = np.random.rand(256, 256, 4).astype(np.float32)
        mask = np.random.randint(0, 3, (256, 256), dtype=np.int32)
        
        image_path = f"datasets/val/images/sample_{i:04d}.npy"
        mask_path = f"datasets/val/masks/sample_{i:04d}.npy"
        
        np.save(image_path, image)
        np.save(mask_path, mask)
    
    print(f"✓ Created 5 validation samples")


def main():
    print("🌍 Deforestation Monitoring - Data Setup")
    print("=" * 60)
    
    setup_directories()
    create_sample_data()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your satellite images to datasets/train/images/")
    print("2. Add corresponding masks to datasets/train/masks/")
    print("3. Run: python training/train.py")
    print("4. Run: python inference/predict.py --model-path checkpoints/best_model.pth --image <image_path>")


if __name__ == "__main__":
    main()
