"""Inference script for deforestation detection."""

import torch
from pathlib import Path
import argparse
import sys
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import DeforestationInference


def main():
    parser = argparse.ArgumentParser(description="Run inference on satellite images")
    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to trained model",
    )
    parser.add_argument(
        "--image",
        type=str,
        help="Path to single image for inference",
    )
    parser.add_argument(
        "--image-dir",
        type=str,
        help="Path to directory of images for batch inference",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="predictions",
        help="Directory to save predictions",
    )
    parser.add_argument(
        "--save-visualization",
        action="store_true",
        help="Save visualization of predictions",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use for inference",
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.image and not args.image_dir:
        print("Error: Provide either --image or --image-dir")
        sys.exit(1)
    
    print("🚀 Deforestation Detection Inference")
    print("=" * 60)
    print(f"Model: {args.model_path}")
    print(f"Device: {args.device}")
    print("=" * 60)
    
    # Create output directory
    Path(args.output_dir).mkdir(exist_ok=True)
    
    # Initialize inference engine
    print("\n📦 Loading model...")
    inference = DeforestationInference(
        model_path=args.model_path,
        device=args.device,
    )
    print("✓ Model loaded")
    
    # Process images
    if args.image:
        print(f"\n🖼️  Processing image: {args.image}")
        mask, stats = inference.predict_image(args.image)
        
        # Save results
        output_path = Path(args.output_dir) / "mask.npy"
        inference.save_prediction(mask, str(output_path))
        
        if args.save_visualization:
            viz_path = Path(args.output_dir) / "visualization.png"
            inference.save_visualization(args.image, mask, str(viz_path))
        
        # Print stats
        print("\n📊 Results:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Save stats
        stats_path = Path(args.output_dir) / "stats.json"
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)
        
        print(f"\n✅ Predictions saved to {args.output_dir}")
    
    elif args.image_dir:
        print(f"\n📁 Processing images from: {args.image_dir}")
        image_paths = list(Path(args.image_dir).glob("*.(jpg|png|tif)"))
        print(f"Found {len(image_paths)} images")
        
        masks, stats_list = inference.predict_batch([str(p) for p in image_paths])
        
        # Save all results
        all_stats = {}
        for i, (mask, stats) in enumerate(zip(masks, stats_list)):
            output_path = Path(args.output_dir) / f"mask_{i:04d}.npy"
            inference.save_prediction(mask, str(output_path))
            
            if args.save_visualization:
                viz_path = Path(args.output_dir) / f"visualization_{i:04d}.png"
                inference.save_visualization(
                    str(image_paths[i]), mask, str(viz_path)
                )
            
            all_stats[f"image_{i:04d}"] = stats
        
        # Save all stats
        stats_path = Path(args.output_dir) / "all_stats.json"
        with open(stats_path, "w") as f:
            json.dump(all_stats, f, indent=2)
        
        print(f"\n✅ Predictions saved to {args.output_dir}")
        print(f"Processed {len(masks)} images")


if __name__ == "__main__":
    main()
