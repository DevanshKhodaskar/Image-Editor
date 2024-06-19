import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance


window = tk.Tk()
window.title("Image Editor")

# Sidebar configuration
sidebar = tk.Frame(window, width=150, bg='#36454F', relief='groove', borderwidth=4)
sidebar.pack(fill='y', side='left')

# Topbar configuration
topbar = tk.Frame(window, bg='#36454F', relief='flat', borderwidth=4, height=50)
topbar.pack(fill='x', side='top')

# Bottombar configuration
bottombar = tk.Frame(window, height=50, bg='#36454F', relief='flat', borderwidth=4)
bottombar.pack(fill='x', side='bottom')

# Main area configuration
mainarea = tk.Frame(window, bg='#2C3A45', relief='sunken', borderwidth=5)
mainarea.pack(fill='both', side='right', expand=True)
mainarea.grid_rowconfigure(0, weight=1)
mainarea.grid_columnconfigure(0, weight=1)

# Global variables to store images and widgets
original_image = None
displayed_image = None
photo_label = None
brightnessScale = None  

def open_image():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg; *.jpeg; *.png; *.gif; *.bmp")])
    return path

def resize_image(image, max_width, max_height):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if original_width > original_height:
        new_width = min(max_width, original_width)
        new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
    else:
        new_height = min(max_height, original_height)
        new_width = int(new_height / aspect_ratio)
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)

    return image.resize((new_width, new_height))

def imageShow():
    global original_image, displayed_image, photo_label
  
    image_path = open_image()
    if image_path:
        original_image = Image.open(image_path)
        displayed_image = resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height())
        photo = ImageTk.PhotoImage(displayed_image)

        # Clear previous image label if exists
        for widget in mainarea.winfo_children():
            widget.destroy()

        photo_label = tk.Label(mainarea, image=photo, bg='#2C3A45')
        photo_label.image = photo
        photo_label.grid(row=0, column=0, sticky='nsew')

        def display_image(event=None):
            global displayed_image
            main_width = mainarea.winfo_width()
            main_height = mainarea.winfo_height()
            displayed_image = resize_image(original_image, main_width, main_height)
            new_photo = ImageTk.PhotoImage(displayed_image)
            photo_label.config(image=new_photo)
            photo_label.image = new_photo

        mainarea.bind('<Configure>', display_image)

def updateBrightness():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global brightnessScale, original_image, displayed_image
    brightImg_container = [None]  # Use a list to store brightImg

    def setBrightness():
        global original_image, displayed_image, photo_label, brightnessScale
    
        # Update the original_image with the new brightness
        original_image = brightImg_container[0]
        
        displayed_image = ImageTk.PhotoImage(original_image)
        
        photo_label.config(image=displayed_image)
        photo_label.image = displayed_image
        
        brightnessScale.destroy()
        applyBrightness.destroy()

    def brightnessControl(value):
        global displayed_image, photo_label, original_image
    
        # Use the original_image for brightness control
        brightEnhancer = ImageEnhance.Brightness(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        brightImg = brightEnhancer.enhance(float(value) / 100)
        
        # Store brightImg in the container
        brightImg_container[0] = brightImg
        
        # Convert brightImg to PhotoImage
        bright_photo = ImageTk.PhotoImage(brightImg)
        
        # Update the photo_label with the new image
        photo_label.config(image=bright_photo)
        photo_label.image = bright_photo
    
    brightnessScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=brightnessControl)
    brightnessScale.set(100)
    brightnessScale.pack()

    applyBrightness = tk.Button(bottombar, text="Apply", command=setBrightness)
    applyBrightness.pack(side='right')


def updateSharpness():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global sharpnessScale,original_image,displayed_image
    sharpImage_container=[None]
    def setSharpness():
        global original_image,displayed_image,photo_label,sharpnessScale
        original_image=sharpImage_container[0]
        displayed_image=ImageTk.PhotoImage(original_image)
        photo_label.config(image=displayed_image)
        photo_label.image=displayed_image
        sharpnessScale.destroy()
        applySharpness.destroy()
    
    
    def sharpnessControl(value):
        global displayed_image, photo_label, original_image
        sharpEnhancer=ImageEnhance.Sharpness(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        sharpImg=sharpEnhancer.enhance(float(value)/100)

        sharpImage_container[0]=sharpImg
        sharp_photo=ImageTk.PhotoImage(sharpImg)

        photo_label.config(image=sharp_photo)
        photo_label.image = sharp_photo

    sharpnessScale = tk.Scale(bottombar, from_=0, to=800, resolution=1, orient='horizontal', length=400, command=sharpnessControl)
    sharpnessScale.set(100)
    sharpnessScale.pack()
    applySharpness = tk.Button(bottombar, text="Apply", command=setSharpness)
    applySharpness.pack(side='right')



def updateSaturation():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global saturationScale, original_image, displayed_image
    saturationImg_container = [None]  # Use a list to store saturationImg

    def setSaturation():
        global original_image, displayed_image, photo_label, saturationScale
    
        # Update the original_image with the new saturation
        original_image = saturationImg_container[0]
        
        displayed_image = ImageTk.PhotoImage(original_image)
        
        photo_label.config(image=displayed_image)
        photo_label.image = displayed_image
        
        saturationScale.destroy()
        applySaturation.destroy()

    def saturationControl(value):
        global displayed_image, photo_label, original_image
    
        # Use the original_image for saturation control
        saturationEnhancer = ImageEnhance.Color(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        saturationImg = saturationEnhancer.enhance(float(value) / 100)
        
        # Store saturationImg in the container
        saturationImg_container[0] = saturationImg
        
        # Convert saturationImg to PhotoImage
        saturation_photo = ImageTk.PhotoImage(saturationImg)
        
        # Update the photo_label with the new image
        photo_label.config(image=saturation_photo)
        photo_label.image = saturation_photo
    
    saturationScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=saturationControl)
    saturationScale.set(100)
    saturationScale.pack()

    applySaturation = tk.Button(bottombar, text="Apply", command=setSaturation)
    applySaturation.pack(side='right')



def updateContrast():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global contrastScale, original_image, displayed_image
    contrastImg_container = [None]  # Use a list to store contrastImg

    def setContrast():
        global original_image, displayed_image, photo_label, contrastScale
    
        # Update the original_image with the new contrast
        original_image = contrastImg_container[0]
        
        displayed_image = ImageTk.PhotoImage(original_image)
        
        photo_label.config(image=displayed_image)
        photo_label.image = displayed_image
        
        contrastScale.destroy()
        applyContrast.destroy()

    def contrastControl(value):
        global displayed_image, photo_label, original_image
    
        # Use the original_image for contrast control
        contrastEnhancer = ImageEnhance.Contrast(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        contrastImg = contrastEnhancer.enhance(float(value) / 100)
        
        # Store contrastImg in the container
        contrastImg_container[0] = contrastImg
        
        # Convert contrastImg to PhotoImage
        contrast_photo = ImageTk.PhotoImage(contrastImg)
        
        # Update the photo_label with the new image
        photo_label.config(image=contrast_photo)
        photo_label.image = contrast_photo
    
    contrastScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=contrastControl)
    contrastScale.set(100)
    contrastScale.pack()

    applyContrast = tk.Button(bottombar, text="Apply", command=setContrast)
    applyContrast.pack(side='right')










# Sidebar buttons
brightness = tk.Button(sidebar, text="Brightness", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17), command=updateBrightness)
brightness.grid(column=0, row=0, pady=5)

sharpness = tk.Button(sidebar, text="Sharpness", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateSharpness)
sharpness.grid(column=0, row=1, pady=5)

saturation = tk.Button(sidebar, text="Saturation", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateSaturation)
saturation.grid(column=0, row=2, pady=5)

contrast = tk.Button(sidebar, text="contrast", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateContrast)
contrast.grid(column=0, row=3, pady=5)

exposure = tk.Button(sidebar, text="Exposure", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17))
exposure.grid(column=0, row=4, pady=5)

vignette = tk.Button(sidebar, text="Vignette", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17))
vignette.grid(column=0, row=5, pady=5)

shadow = tk.Button(sidebar, text="Shadow", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17))
shadow.grid(column=0, row=6, pady=5)

apply = tk.Button(sidebar, text="Apply", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17))
apply.grid(column=0, row=7, pady=5)

# Topbar buttons
openButton = tk.Button(topbar, text="Open", fg='white', bg='gray', font=("Helvetica", 14), command=imageShow)
openButton.pack(side='right', padx=3)
saveButton = tk.Button(topbar, text="Save", fg='white', bg='gray', font=("Helvetica", 14))
saveButton.pack(side='right', padx=3)
resizeButton = tk.Button(topbar, text="Resize", fg='white', bg='gray', font=("Helvetica", 14))
resizeButton.pack(side='left', padx=3)

# Main window configuration
window.geometry("1200x700+0+0")
window.mainloop()
