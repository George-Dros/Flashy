from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
FONT_1 = ("Ariel", 40, "italic")
FONT_2 = ("Ariel", 60, "bold")

random_flash = {}
dict={}

# -----------------------------DATA INPUT------------------------------ #
try:
    data = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dict = original_data.to_dict(orient="records")

else:
    dict = data.to_dict(orient="records")


# -----------------------------RANDOM WORD----------------------------- #


def random_word():
    global random_flash, flip_timer
    window.after_cancel(flip_timer)
    random_flash = choice(dict)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=random_flash["French"], fill='black')
    flip_timer = window.after(3000, func=flip_card)


# -----------------------------FLIP CARD------------------------------- #
def flip_card():

    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word,  text=random_flash["English"], fill="white")

# ---------------------------- REMOVE KNOWN --------------------------- #
def is_known():
    dict.remove(random_flash)
    data = pandas.DataFrame(dict)
    data.to_csv("data/words_to_learn.csv", index=False)

    random_word()

# ---------------------------- UI SETUP ------------------------------- #



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


#Canvas & Flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0,bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400,150, text="", font=FONT_1)
card_word = canvas.create_text(400,263, text="", font=FONT_2)

canvas.grid(row=0,column=0,columnspan=2)


#Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=random_word)
wrong_button.grid(row=1, column=0)

flip_timer = window.after(3000, func=flip_card)

random_word()

window.mainloop()