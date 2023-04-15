import poke_api
from tkinter import *
from tkinter import ttk
import ctypes
import os

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

#make the image cache if not already existing
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the window 
root = Tk()
root.title("Pokemon Image Viewer")
root.minsize(500, 500)


# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


#creating the frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

#adding the image to the frame
img_poke = PhotoImage(file=os.path.join(script_dir, 'poke_image.png'))
lbl_poke = ttk.Label(frame, image=img_poke)
lbl_poke.grid(row = 0, column = 0)

#Adding the pokemon pull-down list (nameS) 
pokemon_name_list = poke_api.get_pokemon_name()
cbox_poke_name = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_name.set("Select A Pokemon")
cbox_poke_name.grid(row = 1, column = 0, padx=10, pady=10)

# Defining the function to handle Pokemon selection from the dropdown list
def handle_pokemon_sel(event):

    #Get the name of the selected pokemon
    pokemon_name = cbox_poke_name.get()
    
    #Download and save the artwork..
    image_poke = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir )
    
    #Display the pokemon artwork
    if image_poke is not None:
        img_poke['file'] = image_poke

    # Enable the 'Set as Desktop Image' button
    btn_set_desktop.state(['!disabled'])

# Binding the handle_pokemon_sel function to the Pokemon dropdown list
cbox_poke_name.bind('<<ComboboxSelected>>', handle_pokemon_sel)

# Creating the 'Set as Desktop Image' button and disabling it 
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image')
btn_set_desktop.grid(row = 2, column = 0, padx=10, pady=10)
btn_set_desktop.state(['disabled'])

# Defining the function to set the selected Pokemon artwork as the desktop image as requested
def set_desktop_image():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, img_poke['file'], 0)

# Finally creating the 'Set as Desktop Image' button and binding it to the set_desktop_image function
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image', command=set_desktop_image)
btn_set_desktop.grid(row = 2, column = 0, padx=10, pady=10)
btn_set_desktop.state(['disabled'])

# Run the mainloop of the main window
root.mainloop()