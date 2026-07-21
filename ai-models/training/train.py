"""Training script for deforestation detection model."""

import torch
from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).parent))

from models import (
    DeforestationDataset,
    DeforestationUNet,
    Trainer,
)


def main():
    parser = argparse.ArgumentParser(description="Train deforestation detection model")
    parser.add_argument(
        "--train-images",
        type=str,
        default="datasets/train/images",
        help="Path to training images directory",
    )
    parser.add_argument(
        "--train-masks",
        type=str,
        default="datasets/train/masks",
        help="Path to training masks directory",
    )
    parser.add_argument(
        "--val-images",
        type=str,
        default="datasets/val/images",
        help="Path to validation images directory",
    )
    parser.add_argument(
        "--val-masks",
        type=str,
        default="datasets/val/masks",
        help="Path to validation masks directory",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=1e-3,
        help="Learning rate",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory to save checkpoints",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use for training",
    )
    
    args = parser.parse_args()
    
    print("🚀 Deforestation Detection Model Training")
    print("=" * 60)
    print(f"Device: {args.device}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.learning_rate}")
    print("=" * 60)
    
    # Create datasets
    print("\n📊 Loading datasets...")
    train_dataset = DeforestationDataset(
        image_dir=args.train_images,
        mask_dir=args.train_masks,
    )
    val_dataset = DeforestationDataset(
        image_dir=args.val_images,
        mask_dir=args.val_masks,
    )
    
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=4,
    )
    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=4,
    )
    
    print(f"✓ Training samples: {len(train_dataset)}")
    print(f"✓ Validation samples: {len(val_dataset)}")
    
    # Create model
    print("\n🏗️  Creating model...")
    model = DeforestationUNet(in_channels=4, num_classes=3)
    print(f"✓ Model created: {model.__class__.__name__}")
    
    # Create trainer
    trainer = Trainer(
        model=model,
        device=args.device,
        learning_rate=args.learning_rate,
    )
    
    # Train
    print("\n🎓 Starting training...")
    trainer.fit(
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=args.epochs,
        checkpoint_dir=args.checkpoint_dir,
    )
    
    print("\n✅ Training completed!")
    print(f"Best model saved to: {args.checkpoint_dir}/best_model.pth")
    print(f"Training history saved to: {args.checkpoint_dir}/training_history.json")


if __name__ == "__main__":
    main()
