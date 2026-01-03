"""
Compute SSIM and PSNR between two images (e.g., cover vs stego).

Usage:
    python stego_metrics.py --ref cover.png --stego stego.png

Requires:
    pip install scikit-image opencv-python
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def load_image(path: Path) -> np.ndarray:
    img_bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError(f"Could not read image: {path}")
    # Convert BGR -> RGB and scale to [0,1] float32 for metrics
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return img_rgb


def compute_metrics(ref_path: Path, stego_path: Path) -> tuple[float, float]:
    ref = load_image(ref_path)
    stego = load_image(stego_path)
    if ref.shape != stego.shape:
        raise ValueError(f"Image shapes differ: {ref.shape} vs {stego.shape}")

    ssim = structural_similarity(ref, stego, channel_axis=2, data_range=1.0)
    psnr = peak_signal_noise_ratio(ref, stego, data_range=1.0)
    return ssim, psnr


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute SSIM and PSNR between two images")
    parser.add_argument("--ref", required=True, help="Reference image (e.g., cover)")
    parser.add_argument("--stego", required=True, help="Stego image to compare")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    ref_path = Path(args.ref)
    stego_path = Path(args.stego)
    ssim, psnr = compute_metrics(ref_path, stego_path)
    print(f"SSIM: {ssim:.6f}")
    print(f"PSNR: {psnr:.2f} dB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

