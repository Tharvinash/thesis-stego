"""
Tkinter UI to compute SSIM and PSNR between two images (cover vs stego).

Requires:
    pip install scikit-image opencv-python

Run:
    python stego_metrics_ui.py
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from stego_metrics import compute_metrics


class MetricsApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("SSIM / PSNR Tester")
        self.master.resizable(False, False)
        self.pack(fill="both", expand=True)

        self.ref_var = tk.StringVar()
        self.stego_var = tk.StringVar()
        self.ssim_var = tk.StringVar(value="SSIM: -")
        self.psnr_var = tk.StringVar(value="PSNR: -")

        self._build_ui()

    def _build_ui(self) -> None:
        # File selection
        files_frame = ttk.LabelFrame(self, text="Images")
        files_frame.pack(fill="x", expand=True, pady=(0, 10))

        ttk.Label(files_frame, text="Reference (cover):").grid(row=0, column=0, sticky="w")
        ttk.Entry(files_frame, textvariable=self.ref_var, width=45).grid(
            row=0, column=1, padx=4, sticky="we"
        )
        ttk.Button(files_frame, text="Browse", command=self._choose_ref).grid(row=0, column=2, padx=2)

        ttk.Label(files_frame, text="Stego:").grid(row=1, column=0, sticky="w")
        ttk.Entry(files_frame, textvariable=self.stego_var, width=45).grid(
            row=1, column=1, padx=4, sticky="we"
        )
        ttk.Button(files_frame, text="Browse", command=self._choose_stego).grid(row=1, column=2, padx=2)

        # Results
        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(fill="x", expand=True, pady=(0, 10))

        ttk.Label(results_frame, textvariable=self.ssim_var, font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(results_frame, textvariable=self.psnr_var, font=("Segoe UI", 10, "bold")).grid(
            row=1, column=0, sticky="w"
        )

        ttk.Button(self, text="Compute", command=self._compute).pack(anchor="e")

    def _choose_ref(self) -> None:
        path = filedialog.askopenfilename(
            title="Select reference image",
            filetypes=[("Images", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff"), ("All files", "*.*")],
        )
        if path:
            self.ref_var.set(path)

    def _choose_stego(self) -> None:
        path = filedialog.askopenfilename(
            title="Select stego image",
            filetypes=[("Images", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff"), ("All files", "*.*")],
        )
        if path:
            self.stego_var.set(path)

    def _compute(self) -> None:
        ref = Path(self.ref_var.get())
        stego = Path(self.stego_var.get())
        if not ref or not stego:
            messagebox.showwarning("Missing files", "Please select both reference and stego images.")
            return
        try:
            ssim, psnr = compute_metrics(ref, stego)
            self.ssim_var.set(f"SSIM: {ssim:.6f}")
            self.psnr_var.set(f"PSNR: {psnr:.2f} dB")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", str(exc))


def main() -> None:
    root = tk.Tk()
    MetricsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

