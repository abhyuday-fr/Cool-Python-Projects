# 🖼️ Image Unblur & Enhancement Tool (Python + Tkinter)

This project is a **Tkinter-based GUI application** that allows users to upload an image and automatically generate:

- ✅ **Unblurred Image** (via Wiener deconvolution)  
- ✅ **Sharpened Image**  
- ✅ **Edge Detected Image** (Canny)  
- ✅ **All output images displayed together**  
- ✅ **Each output image downloadable with a single click**

It uses **OpenCV**, **NumPy**, **scikit-image**, and **Tkinter** to create an easy-to-use desktop tool for enhancing blurry images.

---

## 🚀 Features

### 🔹 1. Image Upload (Tkinter File Dialog)
Choose any JPG/PNG image directly from your computer.

### 🔹 2. Multiple Enhancement Methods
The app automatically generates:

| Enhancement | Description |
|------------|-------------|
| **Deblurred (Wiener Filter)** | Attempts to reverse blur using deconvolution |
| **Sharpened** | Enhances local contrast and edges |
| **Edges Only (Canny)** | Shows highlighted edges only |
| **Original** | Displays original alongside processed ones |

### 🔹 3. Side-by-Side Comparison
All output images appear neatly together inside a scrollable Tkinter window.

### 🔹 4. Download Button
Each processed image has a **Download** button that saves it locally.

---

## 🛠️ Technologies Used

- Python 3.x  
- Tkinter (GUI)  
- OpenCV  
- NumPy  
- scikit-image  
- Pillow (PIL)

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Image-Unblur.git
cd Image-Unblur
```

### 2.Install Depedencies
```
pip install opencv-python numpy pillow scikit-image
```

###3. ▶️ Run the App
```
python image_unblur.py
```

---

## 🧠 How It Works

### 🔸 Deblurring (Wiener Filter)
A Point Spread Function (PSF) is estimated and the blur is reversed using:
```
deconvolved = wiener(image, psf, balance=0.01)
```

### 🔸 Sharpening
OpenCV’s kernel-based filter:
```
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
```

### 🔸 Edge Detection
Standard Canny algorithm:
```
edges = cv2.Canny(image, 100, 200)
```

## 🎯 Future Improvements
- Add zoom & pan for output viewer
- Add more deblurring algorithms
- Add slider-based controls (sharpness, kernel size)

## 📄 License

MIT License — free to use and modify.
