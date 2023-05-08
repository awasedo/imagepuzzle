import random
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Called when a piece is clicked.

def button_click(button):
    global buttons_pressed

    buttons_pressed.append(button)

    if len(buttons_pressed) == 2:
        swap_pieces(buttons_pressed[0], buttons_pressed[1])
        buttons_pressed = []

    elif len(buttons_pressed) == 1:
        image = button.cget("image")
        current_image = Label(small_image_frame, image=image)
        current_image.grid(row=0, column=0)
        current_image.image = image

# Swaps the position of two pieces that are clicked after one another.

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

        for image in small_image_frame.winfo_children():
            image.destroy()

        image = Image.open(initial_image)
        image = image.resize((screen_width, screen_height))
        image = ImageTk.PhotoImage(image)

        background = Label(puzzle_frame, image=image)
        background.grid(row=0, column=0, rowspan=rows, columnspan=columns)
        background.image = image

# Crops an image into rows*columns pieces that are then randomly distributed in a grid.

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

        button = Button(
            puzzle_frame, image=pieces[index],
            border=0, highlightthickness=0, relief="flat")
        button.grid(row=y, column=x)
        button.config(command=lambda button=button: button_click(button))

        buttons.append(button)

        button.image = pieces[index]


def initialize_image(image):
    image = Image.open(image)
    background_image = image.resize((screen_width, screen_height))
    background_image = ImageTk.PhotoImage(background_image)

    background = Label(puzzle_frame, image=background_image)
    background.grid(row=0, column=0, rowspan=rows, columnspan=columns)
    background.image = background_image

    reference_image = image.resize(
        (screen_width//columns, screen_height//rows))
    reference_image = ImageTk.PhotoImage(reference_image)


def open_new_image():
    for item in puzzle_frame.winfo_children():
        item.destroy()

    image = filedialog.askopenfilename(initialdir=os.getcwd())
    initialize_image(image)
    shuffle_image(image, rows, columns)

# This function is called in the difficulty buttons.

def start_puzzle(difficulty):
    for button in puzzle_frame.winfo_children():
        button.destroy()

    image = Image.open(initial_image)
    image = image.resize((screen_width, screen_height))

    if difficulty == 0:
        shuffle_image(image, rows, columns)
    elif difficulty == 1:
        shuffle_image(image, rows, columns)
    elif difficulty == 2:
        shuffle_image(image, rows, columns)

initial_image = "/Users/username/Downloads/image.jpg"

window = Tk()
window.title("Pussel")
window.attributes('-type', 'dialog')

screen_width = 720  # window.winfo_screenwidth()
screen_height = 480  # window.winfo_screenheight()
rows = 3
columns = 3

image = Image.open(initial_image)

buttons_pressed = []
buttons = []

positions = [(x, y) for x in range(columns) for y in range(rows)]

# The Frame that contains the pieces.

puzzle_frame = Frame(window)
puzzle_frame.grid(row=0, column=1, rowspan=rows,
                  columnspan=columns, padx=20, pady=20)

# The Frame that contains the mode buttons.

mode_frame = Frame(window)
mode_frame.grid(row=rows, column=1, padx=20, pady=20, columnspan=columns)

easy_button = Button(mode_frame, text="Easy", command=lambda: start_puzzle(0))
easy_button.grid(row=1, column=0)

normal_button = Button(mode_frame, text="Normal",
                       command=lambda: start_puzzle(1))
normal_button.grid(row=1, column=1)

hard_button = Button(mode_frame, text="Hard", command=lambda: start_puzzle(2))
hard_button.grid(row=1, column=2)

image_button = Button(
    mode_frame, text="Select new image", command=lambda: open_new_image())
image_button.grid(row=0, column=0)

# The Frame that contains the reference image and currently selected images.

small_image_frame = Frame(window)
small_image_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20)

background_image = image.resize((screen_width, screen_height))
background_image = ImageTk.PhotoImage(background_image)

background = Label(puzzle_frame, image=background_image)
background.grid(row=0, column=0, rowspan=rows, columnspan=columns)
background.image = background_image

reference_image = image.resize((screen_width//columns, screen_height//rows))
reference_image = ImageTk.PhotoImage(reference_image)

reference = Label(small_image_frame, image=reference_image)
reference.grid(row=1, column=0)
reference.image = reference_image

window.mainloop()
