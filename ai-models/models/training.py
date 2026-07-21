"""Training pipeline for deforestation detection model."""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from pathlib import Path
import json
from datetime import datetime
from typing import Tuple, Dict, List, Optional
import numpy as np
from tqdm import tqdm


class DeforestationDataset(Dataset):
    """Dataset for deforestation detection."""

    def __init__(
        self,
        image_dir: str,
        mask_dir: str,
        transform=None,
    ):
        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)
        self.transform = transform
        
        # Get list of images
        self.image_files = sorted(list(self.image_dir.glob("*.npy")))
        self.mask_files = sorted(list(self.mask_dir.glob("*.npy")))
        
        assert len(self.image_files) == len(self.mask_files), \
            "Number of images and masks must match"

    def __len__(self) -> int:
        return len(self.image_files)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        image = np.load(self.image_files[idx])
        mask = np.load(self.mask_files[idx])
        
        if self.transform:
            image = self.transform(image)
        
        return (
            torch.from_numpy(image).float(),
            torch.from_numpy(mask).long(),
        )


class DiceCoefficient(nn.Module):
    """Dice coefficient loss function."""

    def __init__(self, smooth: float = 1.0):
        super(DiceCoefficient, self).__init__()
        self.smooth = smooth

    def forward(
        self, predictions: torch.Tensor, targets: torch.Tensor
    ) -> torch.Tensor:
        predictions = torch.softmax(predictions, dim=1)
        intersection = torch.sum(predictions * targets, dim=(2, 3))
        union = torch.sum(predictions, dim=(2, 3)) + torch.sum(targets, dim=(2, 3))
        dice = (2.0 * intersection + self.smooth) / (union + self.smooth)
        return 1.0 - dice.mean()


class CombinedLoss(nn.Module):
    """Combined Cross Entropy + Dice loss."""

    def __init__(self, weight_ce: float = 0.5, weight_dice: float = 0.5):
        super(CombinedLoss, self).__init__()
        self.ce_loss = nn.CrossEntropyLoss()
        self.dice_loss = DiceCoefficient()
        self.weight_ce = weight_ce
        self.weight_dice = weight_dice

    def forward(
        self, predictions: torch.Tensor, targets: torch.Tensor
    ) -> torch.Tensor:
        ce = self.ce_loss(predictions, targets)
        # Convert targets to one-hot for dice loss
        targets_one_hot = torch.nn.functional.one_hot(
            targets, num_classes=predictions.shape[1]
        ).permute(0, 3, 1, 2).float()
        dice = self.dice_loss(predictions, targets_one_hot)
        return self.weight_ce * ce + self.weight_dice * dice


class Trainer:
    """Training handler for deforestation model."""

    def __init__(
        self,
        model: nn.Module,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        learning_rate: float = 1e-3,
        weight_decay: float = 1e-5,
    ):
        self.model = model.to(device)
        self.device = device
        self.optimizer = optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )
        self.criterion = CombinedLoss()
        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": [],
        }

    def train_epoch(self, train_loader: DataLoader) -> Tuple[float, float]:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        total_acc = 0.0
        
        with tqdm(train_loader, desc="Training") as pbar:
            for images, masks in pbar:
                images = images.to(self.device)
                masks = masks.to(self.device)
                
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, masks)
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
                
                # Calculate accuracy
                _, predicted = torch.max(outputs, 1)
                acc = (predicted == masks).float().mean()
                total_acc += acc.item()
                
                pbar.set_postfix({"loss": loss.item(), "acc": acc.item()})
        
        avg_loss = total_loss / len(train_loader)
        avg_acc = total_acc / len(train_loader)
        return avg_loss, avg_acc

    def validate(self, val_loader: DataLoader) -> Tuple[float, float]:
        """Validate model."""
        self.model.eval()
        total_loss = 0.0
        total_acc = 0.0
        
        with torch.no_grad():
            with tqdm(val_loader, desc="Validating") as pbar:
                for images, masks in pbar:
                    images = images.to(self.device)
                    masks = masks.to(self.device)
                    
                    outputs = self.model(images)
                    loss = self.criterion(outputs, masks)
                    
                    total_loss += loss.item()
                    
                    _, predicted = torch.max(outputs, 1)
                    acc = (predicted == masks).float().mean()
                    total_acc += acc.item()
                    
                    pbar.set_postfix({"loss": loss.item(), "acc": acc.item()})
        
        avg_loss = total_loss / len(val_loader)
        avg_acc = total_acc / len(val_loader)
        return avg_loss, avg_acc

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 50,
        checkpoint_dir: str = "checkpoints",
    ):
        """Train model for specified epochs."""
        Path(checkpoint_dir).mkdir(exist_ok=True)
        best_val_loss = float("inf")
        
        for epoch in range(1, epochs + 1):
            print(f"\n\nEpoch {epoch}/{epochs}")
            print("-" * 50)
            
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)
            
            self.history["train_loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_acc"].append(val_acc)
            
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            
            # Save checkpoint if validation loss improves
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                checkpoint_path = Path(checkpoint_dir) / "best_model.pth"
                torch.save(self.model.state_dict(), checkpoint_path)
                print(f"✓ Model saved to {checkpoint_path}")
            
            # Save training history
            history_path = Path(checkpoint_dir) / "training_history.json"
            with open(history_path, "w") as f:
                json.dump(self.history, f, indent=2)

    def save_model(self, path: str):
        """Save model weights."""
        torch.save(self.model.state_dict(), path)
        print(f"Model saved to {path}")

    def load_model(self, path: str):
        """Load model weights."""
        self.model.load_state_dict(torch.load(path))
        print(f"Model loaded from {path}")
