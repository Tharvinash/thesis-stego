# Stego Prototype

Simple tools for hiding text inside images, extracting it, and comparing image quality (SSIM/PSNR). Includes CLIs and Tkinter UIs.

## Prerequisites

- Python 3.10+ recommended
- Windows: use PowerShell; macOS/Linux: similar commands apply

## Setup (virtual environment)

```powershell
cd C:\thesis-prototype
python -m venv .venv
. .venv\Scripts\Activate.ps1   # activates the venv
python -m pip install --upgrade pip
python -m pip install pillow scikit-image opencv-python
```

On PowerShell Core you may need: `Set-ExecutionPolicy -Scope Process Bypass`

## Commands (from project root with venv active)

### 1) CLI: Embed / Extract text

- Embed text into an image (PNG recommended):

```powershell
python stego_tool.py embed --in cover.png --out stego.png --text "secret message"
```

- Extract hidden text:

```powershell
python stego_tool.py extract --in stego.png
```

### 2) GUI: Embed / Extract text

Launch the Tkinter UI:

```powershell
python stego_ui.py
```

Use the buttons to pick a cover image, set an output path, type the secret, and embed. Switch to Extract to recover text from a stego image.

### 3) CLI: SSIM / PSNR metrics

Compare cover vs. stego quality:

```powershell
python stego_metrics.py --ref cover.png --stego stego.png
```

Outputs SSIM (0–1) and PSNR (dB; higher is closer).

### 4) GUI: SSIM / PSNR metrics

Launch the metrics UI:

```powershell
python stego_metrics_ui.py
```

Select the reference (cover) and stego images, then Compute to see SSIM/PSNR.

## Notes and tips

- Use lossless formats (PNG/BMP) for embedding; JPEG may degrade hidden data.
- Keep secrets short enough to fit: capacity is roughly 3 bits per pixel in the cover image.
- The tools read/write standard RGB images; alpha is ignored.
