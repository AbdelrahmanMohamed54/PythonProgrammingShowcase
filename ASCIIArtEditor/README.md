# ASCII Art Editor - Image to Text Conversion GUI

**Author:** Abdelrahman Mohamed

## Description

This Python program is a graphical user interface (GUI) for an ASCII art editor. It allows users to convert images into ASCII text using a set of provided characters. The conversion process includes converting the input image to grayscale and selecting characters based on the similarity to the original image crop. The GUI offers options to specify the image path, character image dimensions, font size, grayscale conversion method, and custom character sets. Users can also save the generated ASCII text to a .txt file.

**Note:** Generating ASCII art may take some time, especially with large character sets, so please be patient.

## Features

- User-friendly GUI for image-to-text conversion.
- Grayscale conversion options: Red Channel, Green Channel, Blue Channel.
- Adjustable character image dimensions and font size.
- Customizable character set for conversion.
- Displays generated ASCII art with scroll bars if necessary.
- Ability to save the generated text to a .txt file.
- Supports JPG image files.

## Prerequisites

Make sure to have the "CONSOLA.TTF" font file in the same directory as this code for proper functionality.

## Usage

1. Select an image by clicking the "Select Image" button.
2. Choose the grayscale conversion method.
3. Enter character image dimensions and font size.
4. Specify a custom character set (optional).
5. Click "Generate ASCII" to convert the image.
6. The generated ASCII art will be displayed in the text area.
7. Use the scroll bars to navigate the ASCII art if needed.
8. Click "Save Text" to save the ASCII art to a .txt file.


## Acknowledgments

- Built using the Tkinter library for GUI.
- Utilizes the Pillow (PIL) library for image processing.

Enjoy creating ASCII art with the ASCII Art Editor! If you have any questions or suggestions, feel free to contact the author.
