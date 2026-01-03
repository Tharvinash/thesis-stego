"""
Compute bits-per-pixel usage and capacity for the LSB stego scheme.

Usage:
    python stego_bpp.py --image cover.png --text "secret"

Assumptions:
- 1 LSB per channel, 3 channels (RGB) => capacity = pixels * 3 bits.
- 32-bit header is used to store message length.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TypedDict

from PIL import Image


class BppResult(TypedDict):
    width: int
    height: int
    pixels: int
    capacity_bits: int
    capacity_bytes: int
    header_bits: int
    payload_bits: int
    total_bits: int
    used_bpp: float
    fits: bool


def compute_bpp(image_path: Path, message: str, bits_per_channel: int = 1, channels: int = 3) -> BppResult:
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = width * height
    capacity_bits = pixels * channels * bits_per_channel
    header_bits = 32
    payload_bits = len(message.encode("utf-8")) * 8
    total_bits = header_bits + payload_bits
    used_bpp = total_bits / pixels if pixels else 0.0
    return {
        "width": width,
        "height": height,
        "pixels": pixels,
        "capacity_bits": capacity_bits,
        "capacity_bytes": capacity_bits // 8,
        "header_bits": header_bits,
        "payload_bits": payload_bits,
        "total_bits": total_bits,
        "used_bpp": used_bpp,
        "fits": total_bits <= capacity_bits,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute BPP usage for stego message")
    parser.add_argument("--image", required=True, help="Cover image path")
    parser.add_argument("--text", required=True, help="Message to evaluate")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = compute_bpp(Path(args.image), args.text)
    print(f"Image: {args.image} ({result['width']}x{result['height']}, pixels={result['pixels']})")
    print(f"Capacity: {result['capacity_bits']} bits ({result['capacity_bytes']} bytes)")
    print(f"Payload: {result['payload_bits']} bits + header {result['header_bits']} bits")
    print(f"Total used: {result['total_bits']} bits ({result['used_bpp']:.4f} bpp)")
    print(f"Fits: {'yes' if result['fits'] else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

