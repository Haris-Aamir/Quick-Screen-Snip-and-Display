import tkinter as tk
from PIL import ImageGrab
import time

# Initialize global variables
start_x = start_y = None  # Coordinates for the starting position
rect = None  # Rectangle object for visual feedback

# Mouse press event to record the starting position
def on_mouse_press(event):
    global start_x, start_y, rect
    start_x, start_y = event.x, event.y  # Record starting mouse position
    
    # Create the rectangle for visual feedback
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='blue', width=1.5, fill = "blue")

# Mouse drag event to update the rectangle
def on_mouse_drag(event):
    global rect
    end_x, end_y = event.x, event.y  # Capture current mouse position
    
    # Update rectangle coordinates during dragging
    canvas.coords(rect, start_x, start_y, end_x, end_y)

# Mouse release event to capture the image
def on_mouse_release(event):
    global start_x, start_y
    
    # Calculate the selected area coordinates (global screen positions)
    x1 = root.winfo_rootx() + min(start_x, event.x)
    y1 = root.winfo_rooty() + min(start_y, event.y)
    x2 = root.winfo_rootx() + max(start_x, event.x)
    y2 = root.winfo_rooty() + max(start_y, event.y)
    
    # Hide the window before capturing
    root.withdraw()  
    time.sleep(0.1)  # Small delay for window to hide
    
    # Capture the selected screen area and save as '12.png'
    captured_image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    captured_image.save("tem567645.png")  # Save the captured image
    #print("Image saved as '12.png'")
    
    # Close the application
    root.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)  # Make the window fullscreen
root.attributes('-alpha', 0.3)        # Set transparency (0.0 to 1.0)
root.configure(cursor="crosshair")        # Set the cursor to a crosshair

# Create a canvas to draw the selection rectangle
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill='both', expand=True)

# Bind mouse events to their respective functions
canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

# Display instructions and run the Tkinter main loop
root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

# Initialize global variables
current_width, current_height = None, None
brightness_factor = 1.0
working_image = None  # To store the current modified state of the image

def on_drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() + (event.x - widget.startX - 500)
    y = widget.winfo_y() + (event.y - widget.startY - 300)
    widget.place(x=x, y=y)

def apply_adjustments():
    """
    Apply both brightness and resizing to the working image,
    and update the displayed image.
    """
    global working_image, tk_image, image_label
    adjusted_image = working_image.copy()

    # Apply brightness
    enhancer = ImageEnhance.Brightness(adjusted_image)
    adjusted_image = enhancer.enhance(brightness_factor)

    # Convert to Tkinter-compatible format
    tk_image = ImageTk.PhotoImage(adjusted_image)
    image_label.config(image=tk_image)

def adjust_brightness(factor):
    """
    Adjust the brightness and reapply adjustments.
    """
    global brightness_factor
    brightness_factor = factor
    apply_adjustments()

def zoom_image(scale_factor):
    """
    Resize the working image and reapply adjustments.
    """
    global working_image, current_width, current_height, tk_image, image_label

    # Calculate new dimensions
    new_width = int(current_width * scale_factor)
    new_height = int(current_height * scale_factor)

    # Enforce minimum size limits
    if new_width < 100 or new_height < 100:
        return  # Prevent image from becoming too small

    # Resize the working image
    working_image = working_image.resize((new_width, new_height))
    current_width, current_height = new_width, new_height

    # Reapply adjustments
    apply_adjustments()

# Create the main Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Load the image
original_image = Image.open("tem567645.png")
current_width, current_height = original_image.size
working_image = original_image.copy()  # Initialize working image
tk_image = ImageTk.PhotoImage(working_image)

# Create a label to display the image
image_label = tk.Label(root, image=tk_image, bg='black')
image_label.place(relx=0.5, rely=0.5, anchor='center')

image_label.bind("<Button-1>", on_drag_start)
image_label.bind("<B1-Motion>", on_drag_motion)

# Close the window when pressing 'ESC'
root.bind("<Escape>", lambda e: root.destroy())

# Background color change bindings
root.bind("<b>", lambda event: root.configure(bg='black'))
root.bind("<w>", lambda event: root.configure(bg='white'))
root.bind("<g>", lambda event: root.configure(bg='grey'))

# Brightness adjustment bindings
root.bind("<h>", lambda event: adjust_brightness(min(brightness_factor + 0.1, 2.0)))
root.bind("<l>", lambda event: adjust_brightness(max(brightness_factor - 0.1, 0.1)))

# Zoom bindings
root.bind("=", lambda event: zoom_image(1.1))  # Scale up by 10%
root.bind("-", lambda event: zoom_image(0.9))  # Scale down by 10%

# Run the Tkinter main loop
root.mainloop()

# Clean up the temporary file
import os
os.remove("tem567645.png")
