import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

# --- ASCII ART CONVERSION LOGIC ---
DEFAULT_CHARSET = "@%#*+=-:. "

def image_to_ascii(image_path, width=100, invert=False):
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    aspect = orig_h / orig_w
    char_aspect = 0.55
    new_h = max(1, int(aspect * width * char_aspect))
    img_resized = img.resize((width, new_h))
    gray = img_resized.convert("L")

    charset = DEFAULT_CHARSET
    n = len(charset)
    ascii_img = []
    pixels = list(gray.getdata())
    rows = [pixels[i*width:(i+1)*width] for i in range(new_h)]

    for row in rows:
        line = ""
        for g in row:
            v = g / 255.0
            if invert:
                v = 1.0 - v
            idx = int(v * (n - 1))
            line += charset[idx]
        ascii_img.append(line)
    return "\n".join(ascii_img)


# --- GUI APPLICATION ---
class ASCIIArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")

        self.image_path = None

        # --- Title ---
        tk.Label(root, text="🎨 ASCII Art Generator", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

        # --- Controls Frame ---
        controls = tk.Frame(root, bg="#1e1e1e")
        controls.pack(pady=5)

        ttk.Button(controls, text="📂 Upload Image", command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Label(controls, text="Width:", bg="#1e1e1e", fg="white").grid(row=0, column=1, padx=5)

        self.width_var = tk.IntVar(value=100)
        tk.Entry(controls, textvariable=self.width_var, width=6).grid(row=0, column=2, padx=5)

        ttk.Button(controls, text="🧮 Generate", command=self.generate_ascii).grid(row=0, column=3, padx=5)
        ttk.Button(controls, text="💾 Save As", command=self.save_ascii).grid(row=0, column=4, padx=5)

        # --- Preview Area ---
        self.preview = tk.Text(root, wrap="none", bg="#0d0d0d", fg="white", font=("Courier", 8))
        self.preview.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        yscroll = tk.Scrollbar(self.preview, command=self.preview.yview)
        xscroll = tk.Scrollbar(self.preview, orient="horizontal", command=self.preview.xview)
        self.preview.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

    def load_image(self):
        path = filedialog.askopenfilename(title="Select an image",
                                          filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.image_path = path
            messagebox.showinfo("Loaded", f"Loaded image:\n{os.path.basename(path)}")

    def generate_ascii(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        width = max(10, self.width_var.get())

        try:
            ascii_art = image_to_ascii(self.image_path, width=width)
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")
            return

        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, ascii_art)

    def save_ascii(self):
        content = self.preview.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No ASCII art to save. Generate one first.")
            return

        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text file", "*.txt"), ("HTML file", "*.html")],
                                            title="Save ASCII Art As")
        if not file:
            return

        if file.endswith(".html"):
            self.save_as_html(file, content)
        else:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Saved ASCII art to {file}")

    def save_as_html(self, file, content):
        html = f"""<!DOCTYPE html>
<html>
<head>
<title>ASCII Art</title>
<style>
body {{
    background-color: #000;
    color: #fff;
    font-family: monospace;
    white-space: pre;
    font-size: 8px;
}}
</style>
</head>
<body>
{content}
</body>
</html>"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)
        messagebox.showinfo("Saved", f"Saved HTML ASCII art to {file}")


# --- MAIN LOOP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtApp(root)
    root.mainloop()
