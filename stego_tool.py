"""
Simple image steganography helper.

- embed: hide UTF-8 text inside an image by tweaking pixel LSBs.
- extract: recover the hidden message.

Usage:
    python stego_tool.py embed --in input.png --out output.png --text "secret"
    python stego_tool.py extract --in output.png

Requires Pillow: pip install pillow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image


def _to_bits(data: bytes) -> Iterable[int]:
    for byte in data:
        for shift in range(7, -1, -1):
            yield (byte >> shift) & 1


def _bits_to_bytes(bits: Iterable[int]) -> bytes:
    out = bytearray()
    current = 0
    count = 0
    for bit in bits:
        current = (current << 1) | bit
        count += 1
        if count == 8:
            out.append(current)
            current = 0
            count = 0
    return bytes(out)


def _pack_length(length: int) -> bytes:
    if length < 0 or length > 0xFFFFFFFF:
        raise ValueError("Message length must fit in 32 bits")
    return length.to_bytes(4, "big")


def _unpack_length(length_bytes: bytes) -> int:
    if len(length_bytes) != 4:
        raise ValueError("Invalid length header")
    return int.from_bytes(length_bytes, "big")


def embed_message(input_path: Path, output_path: Path, message: str) -> None:
    img = Image.open(input_path).convert("RGB")
    pixels = list(img.getdata())

    payload = message.encode("utf-8")
    header = _pack_length(len(payload))
    payload_bits = list(_to_bits(header + payload))

    capacity_bits = len(pixels) * 3  # 3 channels per pixel
    if len(payload_bits) > capacity_bits:
        raise ValueError(
            f"Message too large for image. Capacity={capacity_bits // 8} bytes, "
            f"needed={len(payload_bits) // 8} bytes."
        )

    flat_bits = iter(payload_bits)
    new_pixels = []
    for r, g, b in pixels:
        try:
            r_bit = next(flat_bits)
        except StopIteration:
            new_pixels.append((r, g, b))
            continue
        r = (r & 0xFE) | r_bit

        try:
            g_bit = next(flat_bits)
        except StopIteration:
            new_pixels.append((r, g, b))
            continue
        g = (g & 0xFE) | g_bit

        try:
            b_bit = next(flat_bits)
        except StopIteration:
            new_pixels.append((r, g, b))
            continue
        b = (b & 0xFE) | b_bit

        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def extract_message(input_path: Path) -> str:
    img = Image.open(input_path).convert("RGB")
    pixels = list(img.getdata())

    # Pull bits from channel LSBs
    bits = []
    for r, g, b in pixels:
        bits.extend(((r & 1), (g & 1), (b & 1)))

    # First 32 bits are length
    length_bits = bits[:32]
    message_length = _unpack_length(_bits_to_bytes(length_bits))

    message_bit_count = message_length * 8
    message_bits = bits[32 : 32 + message_bit_count]
    if len(message_bits) < message_bit_count:
        raise ValueError("Image does not contain a complete message.")

    message_bytes = _bits_to_bytes(message_bits)
    return message_bytes.decode("utf-8", errors="replace")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple image LSB steganography")
    sub = parser.add_subparsers(dest="cmd", required=True)

    embed_p = sub.add_parser("embed", help="Embed text into an image")
    embed_p.add_argument("--in", dest="input_path", required=True, help="Path to input image")
    embed_p.add_argument("--out", dest="output_path", required=True, help="Path to write stego image")
    embed_p.add_argument("--text", dest="text", required=True, help="Secret text to embed")

    extract_p = sub.add_parser("extract", help="Extract text from a stego image")
    extract_p.add_argument("--in", dest="input_path", required=True, help="Stego image path")

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    if args.cmd == "embed":
        embed_message(Path(args.input_path), Path(args.output_path), args.text)
        print(f"Embedded {len(args.text.encode('utf-8'))} bytes into {args.output_path}")
        return 0
    if args.cmd == "extract":
        msg = extract_message(Path(args.input_path))
        print(msg)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

