from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#b1ddc6"

# DATA
try:
    vocab_dataframe = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    vocab_dataframe = pandas.read_csv("data/french_words.csv")
vocab_list = vocab_dataframe.to_dict("records")
# random_word = vocab_dataframe.loc[[random.randint(0, 102)]]
# print(random_word.French)
random_word = {}
words_to_learn = {"French": [], "English":[]}


def display_word():
    global random_word, flip_timer
    window.after_cancel(flip_timer)
    random_word = random.choice(vocab_list)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(french_text, text="French", fill="black")
    canvas.itemconfig(english_text, text=random_word["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


# CARD LOGIC
def flip_card():
    global random_word
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(french_text, text="English", fill="white")
    canvas.itemconfig(english_text, text=random_word["English"], fill="white")


def add_word_to_learn():
    # remove known words from current list in program memory, then save that list to a csv each time green button is
    # clicked
    vocab_list.remove(random_word)

    data = pandas.DataFrame(vocab_list)
    # Index add on each save when using this data cyclically
    data.to_csv("data/words_to_learn.csv", index=False)
    display_word()

# CREATE UI
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
french_text = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
english_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")

wrong_button = Button(image=wrong_image, height=93, width=94, highlightthickness=0, command=display_word)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")

right_button = Button(image=right_image, height=93, width=94, highlightthickness=0, command=add_word_to_learn)
right_button.grid(column=1, row=1)

display_word()

window.mainloop()
