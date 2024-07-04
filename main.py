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
bottombar = tk.Frame(window, height=20, bg='#36454F', relief='flat', borderwidth=4,)
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

#Resize image while displayinng

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

#Function to show Image in main area

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


#Function for Resizing Image of resize button

def resize_img():
    global original_image, displayed_image, photo_label
    

    #Function for Resizing
    def ApplyResize():
        global original_image, displayed_image, photo_label
        if original_image:
            resize_height=int(height_label.get())
            resize_width=int(width_label.get())
            resized_image = resize_image(original_image, resize_height, resize_width)
            
            
            displayed_image = ImageTk.PhotoImage(resized_image)
            original_image=resized_image
        
            photo_label.config(image=displayed_image)
            photo_label.image = displayed_image

            height_text.destroy()
            height_label.destroy()
            Width_text.destroy()
            width_label.destroy()
            resize_apply.destroy()

    height_text=tk.Label(topbar,text="Height:",font=('Helvitica',14),fg='white',bg='#36454F')
    height_text.pack(side='left',padx=3)
    
    height_label=tk.Entry(topbar,width=5,font=('arial',14))
    height_label.pack(side='left')
    Width_text=tk.Label(topbar,text="Width:",font=('Helvitica',14),fg='white',bg='#36454F')
    Width_text.pack(side='left',padx=3)
    width_label=tk.Entry(topbar,width=5,font=('arial',14))
    width_label.pack(side='left')
    resize_apply=tk.Button(topbar,text="Apply",font=('Helvitica',14),fg='white', relief='raised', bg='black',command=ApplyResize)
    resize_apply.pack(side='left',padx=10)

    





#Function to update brightness for brightness button

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

    #Connect Brightness to Scale 
    def brightnessControl(value):
        global displayed_image, photo_label, original_image
    
        brightEnhancer = ImageEnhance.Brightness(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        brightImg = brightEnhancer.enhance(float(value) / 100)
        brightImg_container[0] = brightImg
        bright_photo = ImageTk.PhotoImage(brightImg)
        photo_label.config(image=bright_photo)
        photo_label.image = bright_photo
    
    brightnessScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=brightnessControl)
    brightnessScale.set(100)
    brightnessScale.grid(row=0,column=0,padx=200)

    applyBrightness = tk.Button(bottombar, text="Apply",fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17), command=setBrightness)
    applyBrightness.grid(row=0,column=1)

#Function to update sharpness For sharpness Button

def updateSharpness():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global sharpnessScale,original_image,displayed_image
    sharpImage_container=[None] #use list to store
    def setSharpness():
        global original_image,displayed_image,photo_label,sharpnessScale
        original_image=sharpImage_container[0]
        displayed_image=ImageTk.PhotoImage(original_image)
        photo_label.config(image=displayed_image)
        photo_label.image=displayed_image
        sharpnessScale.destroy()
        applySharpness.destroy()
    
    #Connect sharpness to scale
    def sharpnessControl(value):
        global displayed_image, photo_label, original_image
        sharpEnhancer=ImageEnhance.Sharpness(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        sharpImg=sharpEnhancer.enhance(float(value)/100)

        sharpImage_container[0]=sharpImg
        sharp_photo=ImageTk.PhotoImage(sharpImg)

        photo_label.config(image=sharp_photo)
        photo_label.image = sharp_photo

    sharpnessScale = tk.Scale(bottombar, from_=0, to=400, resolution=1, orient='horizontal', length=400, command=sharpnessControl)
    sharpnessScale.set(100)
    sharpnessScale.grid(row=0,column=0,padx=200)
    applySharpness = tk.Button(bottombar, text="Apply",fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17), command=setSharpness)
    applySharpness.grid(row=0,column=1)


#Function to update Saturation for saturation button

def updateSaturation():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global saturationScale, original_image, displayed_image
    saturationImg_container = [None]  # Use a list to store saturationImg

    def setSaturation():
        global original_image, displayed_image, photo_label, saturationScale
    
        original_image = saturationImg_container[0]
        
        displayed_image = ImageTk.PhotoImage(original_image)
        
        photo_label.config(image=displayed_image)
        photo_label.image = displayed_image
        
        saturationScale.destroy()
        applySaturation.destroy()

    #connect with scale
    def saturationControl(value):
        global displayed_image, photo_label, original_image
    
        
        saturationEnhancer = ImageEnhance.Color(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        saturationImg = saturationEnhancer.enhance(float(value) / 100)
        
        
        saturationImg_container[0] = saturationImg
        
        saturation_photo = ImageTk.PhotoImage(saturationImg)
        
        photo_label.config(image=saturation_photo)
        photo_label.image = saturation_photo
    
    saturationScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=saturationControl)
    saturationScale.set(100)
    saturationScale.grid(row=0,column=0,padx=200)

    applySaturation = tk.Button(bottombar, text="Apply",fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17) ,command=setSaturation)
    applySaturation.grid(row=0,column=1)

#Function to Update contrast With contrast button

def updateContrast():
    for widget in bottombar.winfo_children():
        widget.destroy()
    global contrastScale, original_image, displayed_image
    contrastImg_container = [None]  #Use a list to store contrastImg

    def setContrast():
        global original_image, displayed_image, photo_label, contrastScale
    
        # Update the original_image with the new contrast
        original_image = contrastImg_container[0]
        
        displayed_image = ImageTk.PhotoImage(original_image)
        
        photo_label.config(image=displayed_image)
        photo_label.image = displayed_image
        
        contrastScale.destroy()
        applyContrast.destroy()


        #Connect contrast to scale
    def contrastControl(value):
        global displayed_image, photo_label, original_image
    
        contrastEnhancer = ImageEnhance.Contrast(resize_image(original_image, mainarea.winfo_width(), mainarea.winfo_height()))
        contrastImg = contrastEnhancer.enhance(float(value) / 100)
        
        contrastImg_container[0] = contrastImg
        contrast_photo = ImageTk.PhotoImage(contrastImg)
        photo_label.config(image=contrast_photo)
        photo_label.image = contrast_photo
    
    contrastScale = tk.Scale(bottombar, from_=0, to=200, resolution=1, orient='horizontal', length=400, command=contrastControl)
    contrastScale.set(100)
    contrastScale.grid(row=0,column=0,padx=200)

    applyContrast = tk.Button(bottombar, text="Apply",fg='white', relief='raised', bg='black', borderwidth=2, width=8, height=1, font=('Helvetica', 17), command=setContrast)
    applyContrast.grid(row=0,column=1)







# Sidebar buttons
brightness = tk.Button(sidebar, text="Brightness", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17), command=updateBrightness)
brightness.grid(column=0, row=0, pady=25)

sharpness = tk.Button(sidebar, text="Sharpness", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateSharpness)
sharpness.grid(column=0, row=1, pady=25)

saturation = tk.Button(sidebar, text="Saturation", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateSaturation)
saturation.grid(column=0, row=2, pady=25)

contrast = tk.Button(sidebar, text="Contrast", fg='white', relief='raised', bg='black', borderwidth=2, width=10, height=2, font=('Helvetica', 17),command=updateContrast)
contrast.grid(column=0, row=3, pady=25)


#Saveing Function
def img_save():
    global displayed_image
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("All files", "*.*")])
    if file_path:
        image = ImageTk.getimage(displayed_image)
        image.save(file_path)






# Topbar buttons
openButton = tk.Button(topbar, text="Open", fg='white', bg='gray', font=("Helvetica", 14), command=imageShow)
openButton.pack(side='right', padx=3)
saveButton = tk.Button(topbar, text="Save", fg='white', bg='gray', font=("Helvetica", 14),command=img_save)
saveButton.pack(side='right', padx=3)
resizeButton = tk.Button(topbar, text="Resize", fg='white', bg='gray', font=("Helvetica", 14),command=resize_img)
resizeButton.pack(side='left', padx=3)

# Main window configuration
window.geometry("1200x700+0+0")
window.mainloop()
