# 🖼️ Background Remover App (Python + Tkinter + Rembg)

✨ A simple yet powerful **AI-based background remover** built with **Python**, using `rembg`, `Pillow`, and `Tkinter`.  
Easily remove image backgrounds, preview before and after results, and export your processed images — all in one clean, fast, and user-friendly interface!

---

## 🚀 Features

✅ **AI-Powered Background Removal** — Powered by [Rembg](https://github.com/danielgatis/rembg) for accurate results.  
✅ **Drag & Drop Support** — Drop images directly into the app window.  
✅ **Live Preview** — See “Before” and “After” images side-by-side instantly.  
✅ **Color Customization** — Replace background with a custom color using a color picker.  
✅ **Batch Mode (optional)** — Remove backgrounds for multiple files in one go.  
✅ **Loading Animation** — Smooth progress indication during background removal.  
✅ **Export as `.exe`** — Built-in support for packaging with **PyInstaller**.  
✅ **Clean GUI** — Minimalist and responsive design using `Tkinter` and `Pillow`.

---

## 🧠 Tech Stack

| Library | Purpose |
|----------|----------|
| **Tkinter** | Graphical User Interface |
| **rembg** | AI-based background removal |
| **Pillow (PIL)** | Image processing and display |
| **threading** | Smooth non-blocking background processing |
| **io / os** | File handling and memory management |

---

## ⚙️ Installation

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/<your-username>/background-remover.git
cd background-remover
```

### 2️⃣ Install Dependencies
```bash
pip install rembg pillow tkinter
```

### 3️⃣ Run the App
```bash
python main.py
```
