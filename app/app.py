"""
Andrew Kim

8 October 2024

Version `0.0.1`

Quote generator app
"""


import requests

import pandas as pd
import random
import numpy as np
from itertools import chain

import tkinter as tk
from tkinter import ttk, scrolledtext
import sv_ttk

from ciphers import Ciphers


# API Info
KEY = "eRKKQJMvsKi8eZujaeWgcA==KXbzpW6Kq47ozSLX"
URL = "https://api.api-ninjas.com/v1/quotes"



def read_words(filepath: str) -> list:
    """ reads CSV file to obtain words """
    raw = pd.read_csv(filepath)
    return raw["word"].tolist()


WORDS_BY_LENGTH = [read_words(f"./words/{i + 4}_letters.csv") for i in range(6)]
WORDS = read_words("./words/valid.csv")
ISOGRAMS = read_words("./words/isograms.csv")


def random_word(length: int = None) -> str:
    """ Word of random length of specific length greater than 3"""
    if length is None:
        # random_word = ""
        # while len(random_word) != length:
        return random.choice(WORDS)
    elif length <= 0:
        raise ValueError("Invalid word length")
    else:
        return random.choice(WORDS_BY_LENGTH[length - 4])
    


def random_quote(max_length: int = 100) -> tuple:
    """ Gets random quote from API Ninjas"""
    while True:
        response = requests.get(URL, headers={"X-Api-Key": KEY})
        if response.status_code == requests.codes.ok:
            quote_dict = eval(response.text.replace("[", "").replace("]", ""))
            quote = quote_dict["quote"]
            if (
                quote.count(".") < 2 and
                quote.count(",") < 4 and
                len(quote) < max_length and
                not any(char.isdigit() for char in quote)
            ):
                return quote, quote_dict["author"]
        else:
            print("Error: ", response.status_code, response.text)


class CipherGenerator:
    def __init__(self, root):
        self.ciphers = Ciphers()

        self.root = root
        self.root.title("Cipher Generator")

        # default window size
        self.root.geometry("1200x350")

        self.add_elements()

        sv_ttk.set_theme('dark')
        self.root.after(100, lambda: self.root.state('zoomed'))
        


    def add_elements(self):
        """ Add Tkinter elements to GUI """

        # left frame for input descriptions
        self.left_frame = ttk.Frame(self.root, width=160, height=100)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        # right frame for outputs
        self.right_frame = ttk.Frame(self.root, width=120, height=25)
        self.right_frame.grid(row = 0, column=2, padx=10, pady=5)

        # input for columar
        self.label_columnar = ttk.Label(self.left_frame, text="Number of Columnar Transposition ciphers:")
        self.label_columnar.grid(sticky="nw", row=0, column=0, padx=5, pady=5)
        self.entry_columnar = ttk.Entry(self.left_frame, width=15)
        self.entry_columnar.grid(row=0, column=1, padx=5, pady=5)


        # input for fractionated
        self.label_morse = ttk.Label(self.left_frame, text="Number of Fractionated Morse ciphers:")
        self.label_morse.grid(sticky="nw", row=1, column=0, padx=5, pady=5)
        self.entry_morse = ttk.Entry(self.left_frame, width=15)
        self.entry_morse.grid(row=1, column=1, padx=5, pady=5)

        # input for hill 2x2
        self.label_hill_2x2 = ttk.Label(self.left_frame, text="Number of Hill 2x2 ciphers:")
        self.label_hill_2x2.grid(sticky="nw", row=2, column=0, padx=5, pady=5)
        self.entry_hill_2x2 = ttk.Entry(self.left_frame, width=15)
        self.entry_hill_2x2.grid(row=2, column=1, padx=5, pady=5)

        # input for hill 3x3
        self.label_hill_3x3 = ttk.Label(self.left_frame, text="Number of Hill 3x3 ciphers:")
        self.label_hill_3x3.grid(sticky="nw", row=3, column=0, padx=5, pady=5)
        self.entry_hill_3x3 = ttk.Entry(self.left_frame, width=15)
        self.entry_hill_3x3.grid(row=3, column=1, padx=5, pady=5)

        # input for nihilist
        self.label_nihilist = ttk.Label(self.left_frame, text="Number of Nihilist ciphers:")
        self.label_nihilist.grid(sticky="nw", row=4, column=0, padx=5, pady=5)
        self.entry_nihilist = ttk.Entry(self.left_frame, width=15)
        self.entry_nihilist.grid(row=4, column=1, padx=5, pady=5)

        # input for porta
        self.label_porta = ttk.Label(self.left_frame, text="Number of Porta ciphers:")
        self.label_porta.grid(sticky="nw", row=5, column=0, padx=5, pady=5)
        self.entry_porta = ttk.Entry(self.left_frame, width=15)
        self.entry_porta.grid(row=5, column=1, padx=5, pady=5)

        # checkbox for random order
        self.label_randomize = ttk.Label(self.left_frame, text="Randomize order of ciphers?")
        self.label_randomize.grid(sticky="nw", row=6, column=0, padx=5, pady=5)
        self.randomize = tk.BooleanVar()
        self.rand_checkbox = ttk.Checkbutton(self.left_frame, variable=self.randomize)
        self.rand_checkbox.grid(sticky="nw", row=6, column=1, padx=5, pady=5)

        # checkbox for write to text file
        self.label_write = ttk.Label(self.left_frame, text="Write ciphers to text file?")
        self.label_write.grid(sticky="nw", row=7, column=0, padx=5, pady=5)
        self.write_txt = tk.BooleanVar()
        self.write_checkbox = ttk.Checkbutton(self.left_frame, variable=self.write_txt)
        self.write_checkbox.grid(sticky="nw", row=7, column=1, padx=5, pady=5)

        # show filename input for writing to text file
        self.write_path = ttk.Label(self.left_frame, text="Custom filepath: ")
        self.write_path.grid(sticky="nw", row=8, column=0, padx=5, pady=5)
        self.entry_path = ttk.Entry(self.left_frame, width=15)
        self.entry_path.grid(row=8, column=1, padx=5, pady=5)

        # output area
        self.output_area = scrolledtext.ScrolledText(self.right_frame, width=120, height=50)
        self.output_area.pack()

        # generate button
        self.generate_button = ttk.Button(self.left_frame, text="Generate Ciphers", command=self.generate_ciphers)
        self.generate_button.grid(row=9, column=1, padx=5, pady=5)


    
    def add_text(self, text: str):
        """ Adds text to text box """
        self.output_area.insert(tk.END, text)


    def process_question_tuple(self, question_tuple: tuple):
        """ Processes tuple form of question """
        if True:
            return f"""<div class="question">{question_tuple[0]}</div>\n<div class="ciphertext">{question_tuple[1]}</div>\n\n"""
        else:
            return question_tuple[0] + "\n" + question_tuple[1] + "\n\n"


    def generate_ciphers(self):
        """ Generates and displays ciphers """
        try:
            process = lambda input: 0 if input == "" else input
            num_columnar = int(process(self.entry_columnar.get()))
            num_fractionated = int(process(self.entry_morse.get()))
            num_hill_2 = int(process(self.entry_hill_2x2.get()))
            num_hill_3 = int(process(self.entry_hill_3x3.get()))
            num_nihilist = int(process(self.entry_nihilist.get()))
            num_porta = int(process(self.entry_porta.get()))
        except ValueError:
            self.add_text("Invalid input, please enter valid numbers.\n")

        # clear previous putput
        self.output_area.delete(1.0, tk.END)

        # generate ciphers
        questions = []
        questions += [self.process_question_tuple(self.ciphers.columnar(random_quote())) for _ in range(num_columnar)]
        questions += [self.process_question_tuple(self.ciphers.fractionated(random_quote(), random_word())) for _ in range(num_fractionated)]
        questions += [self.process_question_tuple(self.ciphers.hill_2(random_quote())) for _ in range(num_hill_2)]
        questions += [self.process_question_tuple(self.ciphers.hill_3(random_word(), random_word(), random_word())) for _ in range(num_hill_3)]
        questions += [self.process_question_tuple(self.ciphers.nihilist(random_quote(), random_word(), random_word())) for _ in range(num_nihilist)]
        questions += [self.process_question_tuple(self.ciphers.porta(random_quote(), random_word())) for _ in range(num_porta)]

        if self.randomize.get():
            random.shuffle(questions)

        if self.write_txt.get():
            filepath = "output.txt" if self.entry_path.get() == "" else self.entry_path.get()
            if ".txt" not in filepath:
                filepath += "txt"
            f = open(filepath, "w")
            f.riwte("\n".join(questions))
            f.close()

        self.add_text("\n".join(questions))



if __name__ == "__main__":
    root = tk.Tk()
    app = CipherGenerator(root)
    root.mainloop()