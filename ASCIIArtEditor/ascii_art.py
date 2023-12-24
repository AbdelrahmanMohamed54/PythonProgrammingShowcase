"""

Author: Abdelrahman Mohamed

Title: ASCII Art Editor - Image to Text Conversion GUI

Description: This program is a graphical user interface (GUI) for an ASCII art editor.
 It allows users to convert images to ASCII text using a set of provided characters.
 The input image is converted to grayscale, and for each possible position,
 a character is selected based on the lowest distance to the original image crop.
 The conversion process is performed in a separate thread to ensure responsiveness.
 The GUI provides options to specify the image path, character image dimensions, font size,
 and grayscale conversion method. Additionally, users can input their desired character set for the conversion.
 The generated ASCII text is displayed within the GUI, with scroll bars if necessary.
 Users can also save the generated text to a .txt file.

 !!!! PLEASE BE PATIENT AS IT TAKES SOME TIME TO GENERATE THE ASCII ART WHEN YOU PRESS THE GENERATE BUTTON !!!!
 !!!! PLEASE DO NOT USE A CHARACTER SET THAT EXCEEDS 7 CHARACTERS AS IT WILL TAKE FOREVER TO GENERATE THE ASCII ART
  AND MAY NOT WORK!!!!
!!!! PLEASE ONLY USE JPG FILES !!!!
!!!!PLEASE KEEP THE "CONSOLA.TTF" FILE IN THE SAME DIRECTORY AS THIS CODE SO THAT THE CODE CAN WORK CORRECTLY!!!!

"""

import tkinter as tk
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
from tkinter import filedialog, messagebox
import os

character_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+[]{}|;':\",./<>?"
character_set_default = "abcf/.An"


# Grayscale conversion function
def convert_to_grayscale(image, conversion_method):
    if conversion_method == 'Red Channel':
        return image.convert('L', (0.2989, 0.587, 0.114, 0))
    elif conversion_method == 'Green Channel':
        return image.convert('L', (0.2989, 0.587, 0.114, 0))
    elif conversion_method == 'Blue Channel':
        return image.convert('L', (0.2989, 0.587, 0.114, 0))
    else:
        raise ValueError("Invalid conversion method.")


# Character image generation function
def generate_character_images(character_set, width, height, font_size):
    character_images = []
    for character in character_set:
        # Create a new image with white background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(r'CONSOLA.TTF', font_size)  # Use Consolas font

        # Calculate the bounding box of the character
        text_bbox = draw.textbbox((0, 0), character, font=font)

        # Create a new image for the character with white background
        char_img = Image.new('RGB', (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]), color='white')
        draw_char = ImageDraw.Draw(char_img)

        # Calculate the position to center the character in the image
        x = (char_img.width - text_bbox[2] + text_bbox[0]) // 2
        y = (char_img.height - text_bbox[3] + text_bbox[1]) // 2

        # Draw the character on the image
        draw_char.text((x, y), character, fill='black', font=font)
        character_images.append(char_img)
    return character_images


# Distance calculation function
def calculate_distance(image1, image2):
    if image1.mode != 'L':  # Convert image1 to grayscale if it has multiple channels
        image1 = image1.convert('L')
    if image2.mode != 'L':  # Convert image2 to grayscale if it has multiple channels
        image2 = image2.convert('L')

    image1 = np.array(image1)
    image2 = np.array(image2)

    diff = image1 - image2
    distance = np.sqrt(np.sum(diff ** 2))
    return distance


# ASCII art conversion function
def convert_image_to_ascii(image, character_images):
    ascii_text = ''
    for y in range(0, image.height, character_images[0].height):
        for x in range(0, image.width, character_images[0].width):
            crop = image.crop((x, y, x + character_images[0].width, y + character_images[0].height))

            # Resize character images to match the size of the crop image
            resized_character_images = [char_img.resize(crop.size) for char_img in character_images]

            distances = [calculate_distance(crop, char_img) for char_img in resized_character_images]
            closest_character_index = np.argmin(distances)
            ascii_text += character_set[closest_character_index]
        ascii_text += '\n'
    return ascii_text


def display_ascii_text(text):
    # Enable text widget for editing
    ascii_text_display.config(state=tk.NORMAL)
    # Clear existing text
    ascii_text_display.delete('1.0', tk.END)
    # Insert generated ASCII text
    ascii_text_display.insert(tk.END, text)
    # Disable text widget to prevent editing
    ascii_text_display.config(state=tk.DISABLED)


class ConversionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Get values from the GUI components
        self.image_path = os.path.normpath(image_entry.get())
        self.conversion_method = conversion_method.get()
        self.character_set = character_set_entry.get()
        self.width = int(width_entry.get())
        self.height = int(height_entry.get())
        self.font_size = int(font_size_entry.get())

    def run(self):
        image_path = os.path.normpath(image_entry.get())
        width = int(width_entry.get())
        height = int(height_entry.get())
        font_size = int(font_size_entry.get())
        character_set = character_set_entry.get()

        try:
            image = Image.open(image_path)
            grayscale_image = convert_to_grayscale(image, conversion_method.get())
            character_images = generate_character_images(character_set, width, height, font_size)
            ascii_text = convert_image_to_ascii(grayscale_image, character_images)

            # Update GUI with generated ASCII text
            window.after(0, lambda: display_ascii_text(ascii_text))
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Button click handlers
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', ('.jpg', '.jpeg', '.png', '.gif'))])
    print("Selected file path:", file_path)  # Print the file path for debugging
    image_entry.delete(0, tk.END)
    image_entry.insert(tk.END, file_path)


def generate_ascii():
    conversion_thread = ConversionThread()
    conversion_thread.start()


def save_text():
    text_to_save = ascii_text_display.get('1.0', tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '.txt')])
    with open(file_path, 'w') as file:
        file.write(text_to_save)


# Create the main window
window = tk.Tk()
window.title('ASCII Art Editor')

# Create and place GUI components
image_label = tk.Label(window, text='Image Path:')
image_label.grid(row=0, column=0, sticky=tk.W)

image_entry = tk.Entry(window, width=50)
image_entry.insert(tk.END, "example.jpg")  # Default value
image_entry.grid(row=0, column=1, padx=5, pady=5)

image_button = tk.Button(window, text='Select Image', command=select_image)
image_button.grid(row=0, column=2, padx=5, pady=5)

conversion_method_label = tk.Label(window, text='Grayscale Conversion:')
conversion_method_label.grid(row=1, column=0, sticky=tk.W)

conversion_method = tk.StringVar()
conversion_method.set('Red Channel')

conversion_method_radio1 = tk.Radiobutton(window, text='Red Channel', variable=conversion_method, value='Red Channel')
conversion_method_radio1.grid(row=1, column=1, sticky=tk.W)

conversion_method_radio2 = tk.Radiobutton(window, text='Green Channel', variable=conversion_method, value='Green Channel')
conversion_method_radio2.grid(row=1, column=2, sticky=tk.W)

conversion_method_radio3 = tk.Radiobutton(window, text='Blue Channel', variable=conversion_method, value='Blue Channel')
conversion_method_radio3.grid(row=1, column=3, sticky=tk.W)

character_set_label = tk.Label(window, text='Character Set:')
character_set_label.grid(row=2, column=0, sticky=tk.W)

character_set_entry = tk.Entry(window, width=50)
character_set_entry.insert(tk.END, character_set_default)  # Default value
character_set_entry.grid(row=2, column=1, padx=5, pady=5)

width_label = tk.Label(window, text='Character Image Width:')
width_label.grid(row=3, column=0, sticky=tk.W)

width_entry = tk.Entry(window, width=10)
width_entry.insert(tk.END, "10")  # Default value
width_entry.grid(row=3, column=1, padx=5, pady=5)

height_label = tk.Label(window, text='Character Image Height:')
height_label.grid(row=3, column=2, sticky=tk.W)

height_entry = tk.Entry(window, width=10)
height_entry.insert(tk.END, "20")  # Default value
height_entry.grid(row=3, column=3, padx=5, pady=5)

font_size_label = tk.Label(window, text='Font Size:')
font_size_label.grid(row=4, column=0, sticky=tk.W)

font_size_entry = tk.Entry(window, width=10)
font_size_entry.insert(tk.END, "14")  # Default value
font_size_entry.grid(row=4, column=1, padx=5, pady=5)

generate_button = tk.Button(window, text='Generate ASCII', command=generate_ascii)
generate_button.grid(row=5, column=0, padx=5, pady=10)

save_button = tk.Button(window, text='Save Text', command=save_text)
save_button.grid(row=5, column=1, padx=5, pady=10)

# Create a scrollable text widget
frame = tk.Frame(window)
frame.grid(row=6, columnspan=4, padx=5, pady=5)

xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

yscrollbar = tk.Scrollbar(frame)
yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

ascii_text_display = tk.Text(frame, width=80, height=30, state=tk.DISABLED,
                             wrap=tk.NONE,
                             xscrollcommand=xscrollbar.set,
                             yscrollcommand=yscrollbar.set)

ascii_text_display.pack()

xscrollbar.config(command=ascii_text_display.xview)
yscrollbar.config(command=ascii_text_display.yview)

window.mainloop()

