"""
Minimal Tkinter UI for stego_tool.

Allows selecting an image, typing a secret, embedding it, and extracting
hidden text from a stego image. Relies on Pillow. Run with:
    python stego_ui.py
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from stego_tool import embed_message, extract_message


class StegoApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("Stego Helper")
        self.master.resizable(False, False)
        self.pack(fill="both", expand=True)

        self.embed_input_var = tk.StringVar()
        self.embed_output_var = tk.StringVar()
        self.embed_text_var = tk.StringVar()
        self.extract_input_var = tk.StringVar()
        self.extract_output_var = tk.StringVar()

        self._build_embed_section()
        self._build_extract_section()

    def _build_embed_section(self) -> None:
        frame = ttk.LabelFrame(self, text="Embed")
        frame.pack(fill="x", expand=True, pady=(0, 10))

        ttk.Label(frame, text="Cover image:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.embed_input_var, width=45).grid(
            row=0, column=1, padx=4, sticky="we"
        )
        ttk.Button(frame, text="Browse", command=self._choose_cover).grid(row=0, column=2, padx=2)

        ttk.Label(frame, text="Output image:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.embed_output_var, width=45).grid(
            row=1, column=1, padx=4, sticky="we"
        )
        ttk.Button(frame, text="Save As", command=self._choose_output).grid(row=1, column=2, padx=2)

        ttk.Label(frame, text="Secret text:").grid(row=2, column=0, sticky="nw")
        ttk.Entry(frame, textvariable=self.embed_text_var, width=45).grid(
            row=2, column=1, padx=4, pady=4, sticky="we"
        )

        ttk.Button(frame, text="Embed", command=self._handle_embed).grid(
            row=3, column=2, pady=6, sticky="e"
        )

    def _build_extract_section(self) -> None:
        frame = ttk.LabelFrame(self, text="Extract")
        frame.pack(fill="x", expand=True)

        ttk.Label(frame, text="Stego image:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.extract_input_var, width=45).grid(
            row=0, column=1, padx=4, sticky="we"
        )
        ttk.Button(frame, text="Browse", command=self._choose_stego).grid(row=0, column=2, padx=2)

        ttk.Label(frame, text="Recovered:").grid(row=1, column=0, sticky="nw")
        self.extract_output = tk.Text(frame, width=46, height=5, wrap="word")
        self.extract_output.grid(row=1, column=1, padx=4, pady=4, sticky="we")
        ttk.Button(frame, text="Extract", command=self._handle_extract).grid(
            row=1, column=2, padx=2, sticky="ne"
        )

    def _choose_cover(self) -> None:
        path = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Images", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff"), ("All files", "*.*")],
        )
        if path:
            self.embed_input_var.set(path)
            # Suggest default output alongside input
            stem = Path(path).stem
            suggested = str(Path(path).with_name(f"{stem}_stego.png"))
            if not self.embed_output_var.get():
                self.embed_output_var.set(suggested)

    def _choose_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save stego image as",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All files", "*.*")],
        )
        if path:
            self.embed_output_var.set(path)

    def _choose_stego(self) -> None:
        path = filedialog.askopenfilename(
            title="Select stego image",
            filetypes=[("Images", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff"), ("All files", "*.*")],
        )
        if path:
            self.extract_input_var.set(path)

    def _handle_embed(self) -> None:
        try:
            input_path = Path(self.embed_input_var.get())
            output_path = Path(self.embed_output_var.get())
            text = self.embed_text_var.get()
            if not input_path or not output_path or not text:
                messagebox.showwarning("Missing info", "Please select input, output, and secret text.")
                return
            embed_message(input_path, output_path, text)
            messagebox.showinfo("Done", f"Embedded {len(text.encode('utf-8'))} bytes into {output_path}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", str(exc))

    def _handle_extract(self) -> None:
        try:
            input_path = Path(self.extract_input_var.get())
            if not input_path:
                messagebox.showwarning("Missing info", "Please select a stego image.")
                return
            recovered = extract_message(input_path)
            self.extract_output.delete("1.0", tk.END)
            self.extract_output.insert(tk.END, recovered)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", str(exc))


def main() -> None:
    root = tk.Tk()
    StegoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

