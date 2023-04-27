import os
import random
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("Pussel")
window.attributes('-type', 'dialog')

screen_width = 800 #window.winfo_screenwidth()
screen_height = 450 #window.winfo_screenheight()

image_directory = "/Users/eskildarpe/Documents/Projects/pussel/images/"
random_image = random.choice(os.listdir(image_directory))
image = Image.open(image_directory+random_image)
image = image.resize((screen_width, screen_height))

buttons_pressed = []
buttons = []

rows = 3
columns = 3

positions = [(x+2, y) for x in range(columns) for y in range(rows)]

def button_click(button):
    global buttons_pressed
    buttons_pressed.append(button)
    
    if len(buttons_pressed) == 2:
        swap_pieces(buttons_pressed[0], buttons_pressed[1])
        buttons_pressed = []
    
    image = button.cget("image")

    current_image = Label(image=image)
    current_image.grid(row=1, column=1, ipadx=10)
    current_image.image = image

def swap_pieces(piece_1, piece_2):
    piece_1_pos = piece_1.grid_info()
    piece_2_pos = piece_2.grid_info()
    
    piece_1_row = piece_1_pos["row"]
    piece_1_column = piece_1_pos["column"]
    piece_2_row = piece_2_pos["row"]
    piece_2_column = piece_2_pos["column"]
    
    piece_1.grid(row=piece_2_row, column=piece_2_column)
    piece_2.grid(row=piece_1_row, column=piece_1_column)
    
    correct = 0

    for button in buttons:
        button_pos = button.grid_info() 
        button_row = button_pos["row"]         
        button_column = button_pos["column"]         
        button_pos = (button_column, button_row)
        
        index = buttons.index(button)
         
        if button_pos == positions[index]:
            correct += 1

    if correct == rows*columns:
        for button in buttons:
            button.destroy()
        
        image = ImageTk.PhotoImage(image)
        label = Label(window, image=image)
        label.pack() 
        
        label.image = image

def shuffle_image(image, rows, columns):
    width, height = image.size
    piece_width = width // columns
    piece_height = height // rows

    positions = [(x, y) for x in range(columns) for y in range(rows)]
    
    pieces = []
    
    for pos in positions:
        x, y = pos
 
        left = x * piece_width
        top = y * piece_height
        right = (x + 1) * piece_width
        bottom = (y + 1) * piece_height
    
        piece = image.crop((left, top, right, bottom))
        piece = ImageTk.PhotoImage(piece)
        pieces.append(piece)

    random.shuffle(positions)

    for pos in positions:
        index = positions.index(pos)
        x, y = pos

        button = Button(window, image=pieces[index], border=0, highlightthickness=0) 
        button.grid(row=y, column=x+2)
        button.config(command=lambda button=button: button_click(button))
        buttons.append(button)
        button.image = pieces[index]

def start_puzzle(rows, columns):
    shuffle_image(image, rows, columns)

start_puzzle(rows, columns)

image = image.resize((800//3, 450//3))
image = ImageTk.PhotoImage(image)

reference_image = Label(image=image)
reference_image.grid(row=2, column=1)
reference_image.image = image

#frame = Frame(window, width=100, height=screen_height)
#frame.grid(row=0,column=0,padx=20,pady=20)

window.mainloop()
