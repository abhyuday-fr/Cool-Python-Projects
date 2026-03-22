import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from skimage.restoration import wiener, richardson_lucy

# ---------------------------------------------------------
# PSF for deconvolution
# ---------------------------------------------------------
def make_psf(size, sigma):
    x = np.linspace(-size // 2, size // 2, size)
    y = np.linspace(-size // 2, size // 2, size)
    x, y = np.meshgrid(x, y)
    psf = np.exp(-(x**2 + y**2) / (2 * sigma * sigma))
    psf /= psf.sum()
    return psf


# ---------------------------------------------------------
# Image processing functions
# ---------------------------------------------------------
def process_image(path):

    img = cv2.imread(path, 0)
    results = {}
    results["Original"] = img

    # Sharpen
    kernel_sharp = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    results["Sharpened"] = cv2.filter2D(img, -1, kernel_sharp)

    # Unsharp mask
    g = cv2.GaussianBlur(img, (9, 9), 5)
    results["Unsharp Mask"] = cv2.addWeighted(img, 1.5, g, -0.5, 0)

    # High-pass
    big = cv2.GaussianBlur(img, (21, 21), 10)
    hp = cv2.subtract(img, big)
    results["High Pass"] = cv2.addWeighted(img, 1.0, hp, 1.5, 0)

    # Wiener
    psf = make_psf(25, 3)
    wiener_r = np.clip(wiener(img, psf, balance=0.01), 0, 255)
    results["Wiener"] = wiener_r

    # Richardson-Lucy
    rl = richardson_lucy(img, psf, num_iter=30)
    results["Richardson-Lucy"] = rl

    # Edges
    results["Edges - Canny"] = cv2.Canny(img, 50, 150)

    sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    results["Edges - Sobel"] = cv2.magnitude(sx, sy)

    results["Edges - Laplacian"] = cv2.Laplacian(img, cv2.CV_64F)

    return results


# ---------------------------------------------------------
# Save all outputs to a folder
# ---------------------------------------------------------
def save_outputs(results):

    os.makedirs("output_images", exist_ok=True)

    for name, img in results.items():
        filename = f"output_images/{name.replace(' ', '_')}.png"

        # Normalize floating images
        if img.dtype != np.uint8:
            img_to_save = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
            img_to_save = img_to_save.astype(np.uint8)
        else:
            img_to_save = img

        cv2.imwrite(filename, img_to_save)

    print("All output images saved in /output_images/")


# ---------------------------------------------------------
# Show results in a Tkinter window
# ---------------------------------------------------------
def display_results(results):

    for widget in output_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(10, 10), dpi=100)
    cols = 3
    rows = (len(results) + cols - 1) // cols

    i = 1
    for title, image in results.items():
        ax = fig.add_subplot(rows, cols, i)
        ax.imshow(image, cmap="gray")
        ax.set_title(title)
        ax.axis("off")
        i += 1

    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Enable the download button
    download_button.config(state="normal")


# ---------------------------------------------------------
# Select image handler
# ---------------------------------------------------------
def choose_image():
    global processed_results
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.tif")]
    )
    if path:
        processed_results = process_image(path)
        display_results(processed_results)


# ---------------------------------------------------------
# Download button handler
# ---------------------------------------------------------
def download_outputs():
    save_outputs(processed_results)
    os.startfile("output_images")  # Opens the folder on Windows


# ---------------------------------------------------------
# Tkinter GUI
# ---------------------------------------------------------
root = tk.Tk()
root.title("Image Unblur + Sharpen + Edge Detector (Downloadable Outputs)")
root.geometry("1200x900")

title = tk.Label(root, text="Image Processing Comparison Tool",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

btn = tk.Button(root, text="Choose Image", font=("Arial", 14), command=choose_image)
btn.pack(pady=10)

download_button = tk.Button(root, text="Download All Outputs",
                             font=("Arial", 14),
                             command=download_outputs,
                             state="disabled")
download_button.pack(pady=10)

output_frame = tk.Frame(root)
output_frame.pack(fill="both", expand=True)

root.mainloop()
