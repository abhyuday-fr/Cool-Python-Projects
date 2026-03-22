# 🎨 ASCII Art Generator (Python + Tkinter)

Convert any image into beautiful **ASCII art** using a simple and elegant Python GUI.  
This project uses **Pillow** for image processing and **Tkinter** for the graphical interface.  
Supports saving your ASCII art as **.txt** or **.html** files.

---

## 🚀 Features

### ✅ Upload an Image  
Supports **PNG, JPG, JPEG, BMP, WEBP** formats.

### ✅ Generate ASCII Art  
- Converts image to grayscale  
- Resizes intelligently  
- Maps brightness → ASCII characters  
- Adjustable output width  

### ✅ Preview in GUI  
Live ASCII output displayed in a scrollable text window.

### ✅ Save as  
- **Plain text (.txt)**
- **HTML (.html)**  styled with dark background

### 🎨 Clean Dark Themed UI  
Easy to use and beginner friendly.

---

## 🛠️ Requirements

Install dependencies:

```bash
pip install pillow
```

---

## 📦 How to Run
```
python ascii_art.py
```

---

## 🧠 How It Works

1. Image Upload
The program opens a file dialog and stores the selected image path.

2. Convert to Grayscale
Pillow converts RGB image to grayscale for brightness evaluation.

3. Aspect Ratio Fix + Resize
Characters are taller than wide, so resizing includes an aspect ratio correction.

4. Pixel-to-ASCII Mapping
Brightness mapped to characters: @%#*+=-:. 

5. ASCII Display
Rendered in a Tkinter text widget.

6. Save
Export as .txt or .html (monospace pre block).

---

## 🧩 Future Improvements

* Drag-and-drop support

* Colored ASCII output

* Export ASCII as PNG

* Add themes (light/dark toggle)

* Add command-line mode
