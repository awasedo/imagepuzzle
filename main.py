import random
import os
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("Pussel")
window.attributes('-type', 'dialog')

image_directory = "/home/darpe/wallpapers/"
random_image = random.choice(os.listdir(image_directory))
image = Image.open(image_directory+random_image)
image = image.resize((800, 450))

buttons_pressed = []
buttons = []

positions = [(x, y) for y in range(3) for x in range(3)]

def button_click(button):
    global buttons_pressed
    buttons_pressed.append(button)
    
    if len(buttons_pressed) == 2:
        swap_pieces(buttons_pressed[0], buttons_pressed[1])
        buttons_pressed = []

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
    
    if correct == 9:
        for button in buttons:
            button.destroy()
        
        label = Label(window, image=ImageTk.PhotoImage(image))
        label.pack(fill=BOTH, expand=YES)
        

def shuffle_image(image, rows, columns):
    width, height = image.size
    piece_width = width // columns
    piece_height = height // rows

    positions = [(x, y) for y in range(rows) for x in range(columns)]
    
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
        button.grid(row=y, column=x, sticky="nsew")
        button.config(command=lambda button=button: button_click(button))
        buttons.append(button)
        button.image = pieces[index]

def start_puzzle(rows, columns):
    shuffle_image(image, rows, columns)

start_puzzle(3, 3)

window.mainloop()
