# Importing necessary libraries for image processing and GUI creation
import cv2  # For image processing tasks
import numpy as np  # For numerical operations on images
from tkinter import filedialog, Tk, Canvas, Label, Button, font as tkFont, Frame, messagebox, Scrollbar, VERTICAL, HORIZONTAL  # For GUI components and added Scrollbar for detailed image display
from PIL import Image, ImageTk  # For image display in the GUI

# Streamlined error handling for image loading
def load_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image file not found.")
        return image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        exit()

# Efficient image processing using numpy
def process_image(image):
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_range = np.array([0, 0, 100])
        upper_range = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        return mask
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image: {e}")
        exit()

# Direct calculation of severity
def calculate_severity(mask):
    try:
        diseased_pixels = np.count_nonzero(mask)
        total_pixels = mask.size
        severity = (diseased_pixels / total_pixels) * 100
        return severity
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate severity: {e}")
        exit()

# Simplified disease grading
def grade_disease(severity):
    try:
        if severity > 50:
            grade = "severe"
        elif severity > 35:
            grade = "moderate"
        else:
            grade = "mild or healthy"
        messagebox.showinfo("Disease Grade", f"The leaf has a {grade} disease.")
        return grade
    except Exception as e:
        messagebox.showerror("Error", f"Failed to grade disease: {e}")
        exit()

# Enhanced and intuitive GUI design optimized for detailed image display
def gui_detect_and_grade_leaf_disease():
    try:
        root = Tk()
        root.title("Leaf Disease Detection and Grading")
        root.geometry("900x400")  # Adjusted window size for detailed image display

        helv36 = tkFont.Font(family='Helvetica', size=14, weight='bold')  # Adjusted font size for better readability
        canvas = Canvas(root, width=900, height=400, scrollregion=(0, 0, 1500, 1000))  # Adjusted canvas size and scrollregion for detailed image display
        canvas.pack(side="left", fill="both", expand=True)
        
        # Adding scrollbars for detailed image navigation
        vbar = Scrollbar(root, orient=VERTICAL)
        vbar.pack(side="right", fill="y")
        vbar.config(command=canvas.yview)
        hbar = Scrollbar(root, orient=HORIZONTAL)
        hbar.pack(side="bottom", fill="x")
        hbar.config(command=canvas.xview)
        canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        frame = Frame(root)
        frame.place(relx=0.5, rely=0.05, anchor='n')  # Adjusted placement for better alignment

        title = Label(frame, text="Leaf Disease Detection", font=helv36)
        title.pack()

        def open_file():
            filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))  # Added support for JPG files
            if filename:
                image = load_image(filename)
                mask = process_image(image)
                severity = calculate_severity(mask)
                grade = grade_disease(severity)
                display_images(filename, mask)

        def display_images(image_path, mask):
            original_image = Image.open(image_path)
            original_render = ImageTk.PhotoImage(original_image)
            original_img = Label(canvas, image=original_render)
            original_img.image = original_render
            original_img.place(x=30, y=100)  # Adjusted placement for detailed layout
            original_text = Label(canvas, text="Original Image", font=('Helvetica', 10, 'bold'))
            original_text.place(x=30, y=80)  # Placed above the original image for clarity

            threshold_image = Image.fromarray(mask)
            threshold_render = ImageTk.PhotoImage(threshold_image)
            threshold_img = Label(canvas, image=threshold_render)
            threshold_img.image = threshold_render
            threshold_img.place(x=630, y=100)  # Adjusted placement for detailed view
            threshold_text = Label(canvas, text="Threshold Image", font=('Helvetica', 10, 'bold'))
            threshold_text.place(x=630, y=80)  # Placed above the threshold image for clarity

        open_button = Button(root, text="Open Image", command=open_file, font=helv36)
        open_button.pack(side='top', pady=20)  # Adjusted padding for optimal spacing
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize GUI: {e}")
        exit()

# Example usage
if __name__ == "__main__":
    gui_detect_and_grade_leaf_disease()
