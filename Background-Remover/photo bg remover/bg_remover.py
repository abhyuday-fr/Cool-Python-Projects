import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from rembg import new_session,remove
from PIL import Image, ImageTk, ImageOps
import io
import os
import threading

# Create session with bundled model
session = new_session(model_path="u2net.onnx")  # <- uses your local fil

# Global
input_image = None
output_image = None
bg_image_path = None
bg_color_hex = "#FFFFFF"

def select_input_image(path=None):
    if not path:
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
    if path:
        input_path_var.set(path)
        load_preview_image(path)

def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_folder_var.set(folder)

def choose_color():
    global bg_color_hex
    color = colorchooser.askcolor(title="Choose Background Color")
    if color[1]:
        bg_color_hex = color[1]
        color_display.config(bg=bg_color_hex)

def load_preview_image(path):
    global input_image
    try:
        image = Image.open(path).convert("RGBA")
        image.thumbnail((200, 200))
        input_image = ImageTk.PhotoImage(image)
        original_label.config(image=input_image)
        original_label.image = input_image
    except:
        messagebox.showerror("Error", "Cannot load image preview.")

def display_output_preview(pil_image):
    global output_image
    pil_image.thumbnail((200, 200))
    output_image = ImageTk.PhotoImage(pil_image)
    output_label.config(image=output_image)
    output_label.image = output_image

def process_image():
    input_path = input_path_var.get()
    output_folder = output_folder_var.get()
    output_name = output_name_var.get()

    if not input_path or not output_folder or not output_name:
        messagebox.showerror("Missing Info", "Please fill all fields.")
        return

    threading.Thread(target=background_removal_thread,
                     args=(input_path, output_folder, output_name),
                     daemon=True).start()

def background_removal_thread(input_path, output_folder, output_name):
    try:
        show_loading()

        with open(input_path, 'rb') as i:
            input_data = i.read()
            removed_data = remove(input_data, session=session)

        result = Image.open(io.BytesIO(removed_data)).convert("RGBA")

        if bg_mode.get() == "color":
            bg_layer = Image.new("RGBA", result.size, bg_color_hex)
            result = Image.alpha_composite(bg_layer, result)

        elif bg_mode.get() == "image":
            if not bg_image_path:
                raise Exception("No background image selected.")
            bg_img = Image.open(bg_image_path).convert("RGBA")
            bg_img = ImageOps.fit(bg_img, result.size)
            result = Image.alpha_composite(bg_img, result)

        output_path = os.path.join(output_folder, output_name + ".png")

        # Check if file exists and ask before overwriting
        if os.path.exists(output_path):
            response = messagebox.askyesnocancel(
                "File Already Exists",
                f"A file named '{output_name}.png' already exists in the selected folder.\n\n"
                "Do you want to replace it?\n\n"
                "Yes: Replace\nNo: Change the name\nCancel: Cancel saving"
            )
            if response is None:
                hide_loading()
                return  # Cancelled
            elif response is False:
                messagebox.showinfo("Rename Needed", "Please change the output name and try again.")
                hide_loading()
                return  # User chose not to overwrite

        result.save(output_path)

        display_output_preview(result)
        hide_loading()
        messagebox.showinfo("Success", f"Image saved at:\n{output_path}")

    except Exception as e:
        hide_loading()
        messagebox.showerror("Error", str(e))

def show_loading():
    loading_label.place(relx=0.5, rely=0.5, anchor="center")
    root.config(cursor="wait")
    root.update()

def hide_loading():
    loading_label.place_forget()
    root.config(cursor="")
    root.update()

def choose_bg_image():
    global bg_image_path
    path = filedialog.askopenfilename(
        title="Select Background Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if path:
        bg_image_path = path
        bg_image_label.config(text=os.path.basename(path))

def style_button(btn, color="#3498db"):
    btn.config(bg=color, fg="white", activebackground="#2c80b4", activeforeground="white", relief="raised", bd=2, font=("Arial", 10, "bold"))

# GUI Setup
root = tk.Tk()
root.title("AI Background Remover with Custom BG")
root.geometry("720x620")
root.resizable(False, False)

input_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
output_name_var = tk.StringVar()
bg_mode = tk.StringVar(value="transparent")

frame = tk.Frame(root)
frame.pack(pady=10)

# Input
tk.Label(frame, text="Input Image:").grid(row=0, column=0, sticky='e')
tk.Entry(frame, textvariable=input_path_var, width=50).grid(row=0, column=1)
btn_input = tk.Button(frame, text="Browse", command=select_input_image)
btn_input.grid(row=0, column=2, padx=5)
style_button(btn_input)

# Output
tk.Label(frame, text="Output Folder:").grid(row=1, column=0, sticky='e')
tk.Entry(frame, textvariable=output_folder_var, width=50).grid(row=1, column=1)
btn_output = tk.Button(frame, text="Choose", command=select_output_folder)
btn_output.grid(row=1, column=2, padx=5)
style_button(btn_output)

tk.Label(frame, text="Output File Name:").grid(row=2, column=0, sticky='e')
tk.Entry(frame, textvariable=output_name_var, width=50).grid(row=2, column=1)

# BG Options
tk.Label(frame, text="Background Option:").grid(row=3, column=0, sticky='e')
tk.Radiobutton(frame, text="Transparent", variable=bg_mode, value="transparent").grid(row=3, column=1, sticky='w')
tk.Radiobutton(frame, text="Solid Color", variable=bg_mode, value="color").grid(row=4, column=1, sticky='w')
color_display = tk.Label(frame, text="       ", bg=bg_color_hex, relief="sunken", width=10)
color_display.grid(row=4, column=2)
btn_color = tk.Button(frame, text="Pick Color", command=choose_color)
btn_color.grid(row=4, column=3)
style_button(btn_color, "black")

tk.Radiobutton(frame, text="Image", variable=bg_mode, value="image").grid(row=5, column=1, sticky='w')
btn_bg_img = tk.Button(frame, text="Choose BG Image", command=choose_bg_image)
btn_bg_img.grid(row=5, column=2)
style_button(btn_bg_img, "red")

bg_image_label = tk.Label(frame, text="", fg="gray")
bg_image_label.grid(row=6, column=1, sticky="w")

# Process button
btn_process = tk.Button(root, text="Remove Background", command=process_image)
btn_process.pack(pady=15)
style_button(btn_process, "#27ae60")

# Previews
preview_frame = tk.Frame(root)
preview_frame.pack()

tk.Label(preview_frame, text="Original").grid(row=0, column=0)
tk.Label(preview_frame, text="Processed").grid(row=0, column=1)

original_label = tk.Label(preview_frame)
original_label.grid(row=1, column=0, padx=20, pady=10)

output_label = tk.Label(preview_frame)
output_label.grid(row=1, column=1, padx=20, pady=10)

# Loading
loading_label = tk.Label(root, text="Processing...", font=("Arial", 14), fg="blue")

tk.Label(root, text="Created with rembg + Pillow", font=("Arial", 8), fg="gray").pack(side='bottom', pady=5)

root.mainloop()
