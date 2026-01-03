"""
Tkinter UI to estimate bits-per-pixel (BPP) usage for a secret message
with the LSB stego scheme (1 LSB per RGB channel).

Run:
    python stego_bpp_ui.py
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from stego_bpp import compute_bpp


class BppApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("BPP Estimator")
        self.master.resizable(False, False)
        self.pack(fill="both", expand=True)

        self.image_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.result_vars = {
            "resolution": tk.StringVar(value="Resolution: -"),
            "capacity": tk.StringVar(value="Capacity: -"),
            "payload": tk.StringVar(value="Payload: -"),
            "total": tk.StringVar(value="Total used: -"),
            "bpp": tk.StringVar(value="BPP: -"),
            "fits": tk.StringVar(value="Fits: -"),
        }

        self._build_ui()

    def _build_ui(self) -> None:
        files_frame = ttk.LabelFrame(self, text="Inputs")
        files_frame.pack(fill="x", expand=True, pady=(0, 10))

        ttk.Label(files_frame, text="Cover image:").grid(row=0, column=0, sticky="w")
        ttk.Entry(files_frame, textvariable=self.image_var, width=45).grid(
            row=0, column=1, padx=4, sticky="we"
        )
        ttk.Button(files_frame, text="Browse", command=self._choose_image).grid(row=0, column=2, padx=2)

        ttk.Label(files_frame, text="Secret text:").grid(row=1, column=0, sticky="w")
        ttk.Entry(files_frame, textvariable=self.text_var, width=45).grid(
            row=1, column=1, padx=4, pady=4, sticky="we"
        )

        ttk.Button(self, text="Compute BPP", command=self._compute).pack(anchor="e", pady=(0, 10))

        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(fill="x", expand=True)

        ttk.Label(results_frame, textvariable=self.result_vars["resolution"]).grid(row=0, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.result_vars["capacity"]).grid(row=1, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.result_vars["payload"]).grid(row=2, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.result_vars["total"]).grid(row=3, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.result_vars["bpp"]).grid(row=4, column=0, sticky="w")
        ttk.Label(results_frame, textvariable=self.result_vars["fits"]).grid(row=5, column=0, sticky="w")

    def _choose_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Images", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff"), ("All files", "*.*")],
        )
        if path:
            self.image_var.set(path)

    def _compute(self) -> None:
        image_path = Path(self.image_var.get())
        text = self.text_var.get()
        if not image_path or not text:
            messagebox.showwarning("Missing input", "Please select a cover image and enter secret text.")
            return
        try:
            res = compute_bpp(image_path, text)
            self.result_vars["resolution"].set(
                f"Resolution: {res['width']} x {res['height']} (pixels={res['pixels']})"
            )
            self.result_vars["capacity"].set(
                f"Capacity: {res['capacity_bits']} bits ({res['capacity_bytes']} bytes)"
            )
            self.result_vars["payload"].set(
                f"Payload: {res['payload_bits']} bits + header {res['header_bits']} bits"
            )
            self.result_vars["total"].set(f"Total used: {res['total_bits']} bits")
            self.result_vars["bpp"].set(f"BPP: {res['used_bpp']:.4f} bits/pixel")
            self.result_vars["fits"].set(f"Fits: {'yes' if res['fits'] else 'no'}")
            if not res["fits"]:
                messagebox.showwarning("Too large", "Message does not fit in this image with 1 LSB per channel.")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", str(exc))


def main() -> None:
    root = tk.Tk()
    BppApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

