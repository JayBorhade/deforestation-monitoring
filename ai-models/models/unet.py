"""U-Net model architecture for deforestation detection."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple


class DoubleConv(nn.Module):
    """Double convolution block: Conv -> BatchNorm -> ReLU -> Conv -> BatchNorm -> ReLU."""

    def __init__(self, in_channels: int, out_channels: int):
        super(DoubleConv, self).__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.double_conv(x)


class DownBlock(nn.Module):
    """Down sampling block: MaxPool -> DoubleConv."""

    def __init__(self, in_channels: int, out_channels: int):
        super(DownBlock, self).__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.maxpool_conv(x)


class UpBlock(nn.Module):
    """Up sampling block: Upsample -> DoubleConv."""

    def __init__(self, in_channels: int, out_channels: int):
        super(UpBlock, self).__init__()
        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
        self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        # Concatenate skip connection
        x = torch.cat([x, skip], dim=1)
        return self.conv(x)


class UNet(nn.Module):
    """U-Net architecture for semantic segmentation.
    
    Input: (batch, channels, height, width)
    Output: (batch, num_classes, height, width)
    """

    def __init__(self, in_channels: int = 3, num_classes: int = 2, features: List[int] = None):
        super(UNet, self).__init__()
        if features is None:
            features = [64, 128, 256, 512]

        self.in_channels = in_channels
        self.num_classes = num_classes
        self.features = features

        # Encoder (Down path)
        self.initial_conv = DoubleConv(in_channels, features[0])
        self.down1 = DownBlock(features[0], features[1])
        self.down2 = DownBlock(features[1], features[2])
        self.down3 = DownBlock(features[2], features[3])

        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(features[3], features[3] * 2),
        )

        # Decoder (Up path)
        self.up3 = UpBlock(features[3] * 2 + features[3], features[3])
        self.up2 = UpBlock(features[3] + features[2], features[2])
        self.up1 = UpBlock(features[2] + features[1], features[1])
        self.up0 = UpBlock(features[1] + features[0], features[0])

        # Final output layer
        self.final_conv = nn.Conv2d(features[0], num_classes, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Encoder
        skip0 = self.initial_conv(x)
        skip1 = self.down1(skip0)
        skip2 = self.down2(skip1)
        skip3 = self.down3(skip2)

        # Bottleneck
        bottleneck = self.bottleneck(skip3)

        # Decoder
        up3 = self.up3(bottleneck, skip3)
        up2 = self.up2(up3, skip2)
        up1 = self.up1(up2, skip1)
        up0 = self.up0(up1, skip0)

        # Final output
        output = self.final_conv(up0)
        return output


class DeforestationUNet(nn.Module):
    """U-Net specialized for deforestation detection with 3 output classes.
    
    Classes:
    - 0: Forest
    - 1: Deforestation
    - 2: Degradation
    """

    def __init__(self, in_channels: int = 4, num_classes: int = 3):
        super(DeforestationUNet, self).__init__()
        self.unet = UNet(in_channels=in_channels, num_classes=num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.unet(x)


def create_unet(in_channels: int = 3, num_classes: int = 2) -> UNet:
    """Factory function to create a U-Net model."""
    return UNet(in_channels=in_channels, num_classes=num_classes)


def create_deforestation_unet(in_channels: int = 4, num_classes: int = 3) -> DeforestationUNet:
    """Factory function to create a deforestation-specific U-Net model."""
    return DeforestationUNet(in_channels=in_channels, num_classes=num_classes)
