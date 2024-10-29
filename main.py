"""Liam Meisinger's Image Watermarking program"""

import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

"""Window"""
window = tk.Tk()
window.title("Watermark App")
window.config(bg="#f0f0f0")
window.minsize(300, 150)

"""Global variables for watermark settings"""
watermark_color = "#ffffff"
watermark_size = 16
watermark_opacity = 255
watermark_font = "arial.ttf"

"""Functions"""


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img, img_display, img_copy
        img = Image.open(file_path).convert("RGBA")
        img_copy = img.copy().convert("RGBA")
        img_display = ImageTk.PhotoImage(img)
        image_label.config(image=img_display)
        image_label.image = img_display
        update_preview()


def update_preview(*args):
    if img:
        preview_img = img.copy().convert("RGBA")
        draw = ImageDraw.Draw(preview_img, "RGBA")
        font = ImageFont.truetype(watermark_font, watermark_size)
        color_with_opacity = watermark_color + format(watermark_opacity, '02x')

        # Get bounding box and calculate position
        text_bbox = draw.textbbox((0, 0), entry.get(), font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = img.width - text_width - 10
        y = img.height - text_height - 10
        draw.text((x, y), entry.get(), fill=color_with_opacity, font=font)

        # Update the image label with the preview
        preview_img_display = ImageTk.PhotoImage(preview_img)
        image_label.config(image=preview_img_display)
        image_label.image = preview_img_display


def apply_watermark():
    draw = ImageDraw.Draw(img, "RGBA")
    font = ImageFont.truetype(watermark_font, watermark_size)
    color_with_opacity = watermark_color + format(watermark_opacity, '02x')

    text_bbox = draw.textbbox((0, 0), entry.get(), font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = img.width - text_width - 10
    y = img.height - text_height - 10
    draw.text((x, y), entry.get(), fill=color_with_opacity, font=font)

    img_display = ImageTk.PhotoImage(img)
    image_label.config(image=img_display)
    image_label.image = img_display


def save_image():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        img.save(save_path)

"""New Window for settings"""
def open_settings_window():
    settings_window = tk.Toplevel(window)
    settings_window.minsize(300, 200)
    settings_window.title("Settings")

    # Font size setting
    tk.Label(settings_window, text="Font Size").pack()
    size_slider = tk.Scale(settings_window, from_=10, to=100, orient="horizontal", command=lambda v: update_size(v))
    size_slider.set(watermark_size)
    size_slider.pack()

    # Color picker
    tk.Label(settings_window, text="Font Color").pack()
    color_button = tk.Button(settings_window, text="Choose Color", command=choose_color)
    color_button.pack()

    # Opacity setting
    tk.Label(settings_window, text="Opacity").pack()
    opacity_slider = tk.Scale(settings_window, from_=0, to=255, orient="horizontal", command=lambda v: update_opacity(v))
    opacity_slider.set(watermark_opacity)
    opacity_slider.pack()

def choose_color():
    global watermark_color
    color_code = colorchooser.askcolor(title="Choose watermark color")[1]
    if color_code:
        watermark_color = color_code
        update_preview()

def update_size(value):
    global watermark_size
    watermark_size = int(value)
    update_preview()

def update_opacity(value):
    global watermark_opacity
    watermark_opacity = int(value)
    update_preview()


"""Buttons"""

open_button = tk.Button(window, text="Open Image", command=open_image, bg="#28b463")
apply_button = tk.Button(window, text="Apply Watermark", command=apply_watermark, bg="#3498db")
save_button = tk.Button(window, text="Save Image", command=save_image, bg="#3498db")
settings_button = tk.Button(window, text="Settings", command=open_settings_window, bg="#f39c12")
entry = tk.Entry(width=30)
entry.insert(tk.END, string="LiamMeisinger")

entry.bind("<KeyRelease>", update_preview) #Update preview on release

"""Positions"""
image_label = tk.Label(window)
image_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
entry.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
open_button.grid(row=3, column=0, padx=10, pady=10)
apply_button.grid(row=3, column=2, padx=10, pady=10)
save_button.grid(row=3, column=3, padx=10, pady=10)
settings_button.grid(row=3, column=1, padx=10, pady=10)

window.mainloop()
