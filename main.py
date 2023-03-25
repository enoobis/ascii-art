from tkinter import *
from tkinter import filedialog
from PIL import Image
import numpy as np

# Define the character set to use for the ASCII art
CHARACTER_SET = np.asarray(list(' .,:irs?@9B&#'))

def upload_image():
    # Open a file dialog to allow the user to select an image file
    filename = filedialog.askopenfilename(initialdir="", title="Select file",
                                          filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))

    # Load the selected image and convert it to grayscale
    image = Image.open(filename).convert('L')

    # Resize the image to a smaller size to create the ASCII art
    width, height = image.size
    aspect_ratio = height / float(width)
    new_width = 120
    new_height = int(aspect_ratio * new_width * 0.55)
    new_image = image.resize((new_width, new_height))

    # Convert the resized image to a numpy array and normalize its values
    pixels = np.array(new_image.getdata()).reshape((new_height, new_width))
    pixels = pixels / 255.0

    # Map the pixel values to characters from the character set
    characters = CHARACTER_SET[(np.round(pixels * (len(CHARACTER_SET) - 1))).astype(int)]

    # Create the ASCII art string
    ascii_art = "\n".join("".join(row) for row in characters)

    # Save the ASCII art as a text file
    with open("output.txt", "w") as text_file:
        text_file.write(ascii_art)

    # Convert the ASCII art to an image and save it as a PNG file
    new_image = Image.fromarray((CHARACTER_SET == characters[...,None]).all(axis=-1).astype(int) * 255, 'L')
    new_image.save("output.png")

    # Display the ASCII art in a label
    ascii_art_label.config(text=ascii_art)

# Create the main window and add a button to upload an image
root = Tk()
root.title("ASCII Art Generator")

upload_button = Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# Add a label to display the ASCII art
ascii_art_label = Label(root, font=("Courier New", 8))
ascii_art_label.pack()

root.mainloop()