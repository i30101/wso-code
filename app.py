# Author: Andrew Kim
# Version: 2.1.0
# Since: 26 March 2024
# Cipher text generator app

# import external libraries
import random
import requests
import numpy as np
from itertools import chain
import tkinter as tk
from tkinter import scrolledtext



# API info
KEY = "eRKKQJMvsKi8eZujaeWgcA==KXbzpW6Kq47ozSLX"
URL = "https://api.api-ninjas.com/v1/"

# check if word is isogram
def is_isogram(word: str) -> bool:
    return [word.count(letter) for letter in word] == [1 for n in word]


# get random word 
def random_word(isogram: bool = True, min: int = 4, max: int = 8) -> str:
    word_api = URL + "randomword"
    while True:
        # get word from API
        response = requests.get(word_api, headers={"X-Api-Key": KEY})
        if response.status_code == requests.codes.ok:
            # format raw text
            response = response.text.replace("{\"word\": \"", "").replace("\"}", "")

            # word is proper length
            if min <= len(response) <= max:
                # isogram not desired or isogram desired and word is isogram
                if not isogram or is_isogram(response):
                    return response


# get random quote
def random_quote(max_length: int = 100) -> tuple:
    quote_api = URL + "quotes"
    while True:
        response = requests.get(quote_api, headers={'X-Api-Key': KEY})
        if response.status_code == requests.codes.ok:
            quote_dict = eval(response.text.replace("[", "").replace("]", ""))
            quote = quote_dict["quote"]
            if (
                quote.count(".") < 2 and        # less than two sentences
                quote.count(",") < 4 and        # less than four commas
                len(quote) < max_length and     # less than 100 characters
                not any(char.isdigit() for char in quote)   # quote does not have numbers
            ):
                return quote, quote_dict["author"]
        else:
            print("Error: ", response.status_code, response.text)


# tkinter interface for generating ciphers
class CipherGeneratorApp:
    def __init__(self, master):
        # cipher generator
        self.ciphers = Ciphers()

        self.master = master
        self.master.title("kt + mango cipher generator")

        # default window size
        self.master.geometry("1200x350")

        # left frame for input descriptions
        self.left_frame = tk.Frame(master, width=160, height=100)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        # right frame for outputs
        self.right_frame = tk.Frame(master, width=120, height=25)
        self.right_frame.grid(row=0, column=2, padx=10, pady=5)


        # input for columar
        self.label_columnar = tk.Label(self.left_frame, text="Number of Columnar Transposition ciphers:")
        self.label_columnar.grid(sticky="nw", row=0, column=0, padx=5, pady=5)
        self.entry_columnar = tk.Entry(self.left_frame, width=15)
        self.entry_columnar.grid(row=0, column=1, padx=5, pady=5)


        # input for fractionated
        self.label_morse = tk.Label(self.left_frame, text="Number of Fractionated Morse ciphers:")
        self.label_morse.grid(sticky="nw", row=1, column=0, padx=5, pady=5)
        self.entry_morse = tk.Entry(self.left_frame, width=15)
        self.entry_morse.grid(row=1, column=1, padx=5, pady=5)

        # input for hill 2x2
        self.label_hill_2x2 = tk.Label(self.left_frame, text="Number of Hill 2x2 ciphers:")
        self.label_hill_2x2.grid(sticky="nw", row=2, column=0, padx=5, pady=5)
        self.entry_hill_2x2 = tk.Entry(self.left_frame, width=15)
        self.entry_hill_2x2.grid(row=2, column=1, padx=5, pady=5)

        # input for hill 3x3
        self.label_hill_3x3 = tk.Label(self.left_frame, text="Number of Hill 3x3 ciphers:")
        self.label_hill_3x3.grid(sticky="nw", row=3, column=0, padx=5, pady=5)
        self.entry_hill_3x3 = tk.Entry(self.left_frame, width=15)
        self.entry_hill_3x3.grid(row=3, column=1, padx=5, pady=5)

        # input for nihilist
        self.label_nihilist = tk.Label(self.left_frame, text="Number of Nihilist ciphers:")
        self.label_nihilist.grid(sticky="nw", row=4, column=0, padx=5, pady=5)
        self.entry_nihilist = tk.Entry(self.left_frame, width=15)
        self.entry_nihilist.grid(row=4, column=1, padx=5, pady=5)

        # input for porta
        self.label_porta = tk.Label(self.left_frame, text="Number of Porta ciphers:")
        self.label_porta.grid(sticky="nw", row=5, column=0, padx=5, pady=5)
        self.entry_porta = tk.Entry(self.left_frame, width=15)
        self.entry_porta.grid(row=5, column=1, padx=5, pady=5)

        # checkbox for random order
        self.label_randomize = tk.Label(self.left_frame, text="Randomize order of ciphers?")
        self.label_randomize.grid(sticky="nw", row=6, column=0, padx=5, pady=5)
        self.randomize = tk.BooleanVar()
        self.rand_checkbox = tk.Checkbutton(self.left_frame, variable=self.randomize)
        self.rand_checkbox.grid(sticky="nw", row=6, column=1, padx=5, pady=5)

        # checkbox for write to text file
        self.label_write = tk.Label(self.left_frame, text="Write ciphers to text file?")
        self.label_write.grid(sticky="nw", row=7, column=0, padx=5, pady=5)
        self.write_txt = tk.BooleanVar()
        self.write_checkbox = tk.Checkbutton(self.left_frame, variable=self.write_txt)
        self.write_checkbox.grid(sticky="nw", row=7, column=1, padx=5, pady=5)

        # show filename input for writing to text file
        self.write_path = tk.Label(self.left_frame, text="Custom filepath: ")
        self.write_path.grid(sticky="nw", row=8, column=0, padx=5, pady=5)
        self.entry_path = tk.Entry(self.left_frame, width=15)
        self.entry_path.grid(row=8, column=1, padx=5, pady=5)

        # output area
        self.output_area = scrolledtext.ScrolledText(self.right_frame, width=98, height=20)
        self.output_area.pack()

        # # generate button
        self.generate_button = tk.Button(self.left_frame, text="Generate Ciphers", command=self.generate_ciphers)
        self.generate_button.grid(row=9, column=1, padx=5, pady=5)


    def generate_ciphers(self):
        try:
            process = lambda input : 0 if input == "" else input
            num_columnar = int(process(self.entry_columnar.get()))
            num_fractionated = int(process(self.entry_morse.get()))
            num_hill_2 = int(process(self.entry_hill_2x2.get()))
            num_hill_3 = int(process(self.entry_hill_3x3.get()))
            num_nihilist = int(process(self.entry_nihilist.get()))
            num_porta = int(process(self.entry_porta.get()))
        except ValueError:
            self.output_area.insert(tk.END, "Invalid input. Please enter valid numbers.\n")
            return

        # Clear previous output
        self.output_area.delete(1.0, tk.END)

        # Generate ciphers
        questions = []
        questions += [self.ciphers.columnar() for _ in range(num_columnar)]
        questions += [self.ciphers.fractionated() for _ in range(num_fractionated)]
        questions += [self.ciphers.hill_2() for _ in range(num_hill_2)]
        questions += [self.ciphers.hill_3() for _ in range(num_hill_3)]
        questions += [self.ciphers.nihilist() for _ in range(num_nihilist)]
        questions += [self.ciphers.porta() for _ in range(num_porta)]

        if self.randomize.get():
            random.shuffle(questions)

        if self.write_txt.get():
            filepath = "output.txt" if self.entry_path.get() == "" else self.entry_path.get()
            if ".txt" not in filepath:
                filepath += ".txt"
            f = open(filepath, "w")
            f.write("\n".join(questions))
            f.close()

        # Display ciphers in the output area
        self.output_area.insert(tk.END, "\n".join(questions))



# ciphertext string generator
class Ciphers:
    def __init__(self):
        # alphabet
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # punctuation characters
        self.PUNCTUATION = '''!()-[]{};:'"\,,<>./?@#$%^&*_~'''

        # morse chart
        self.MORSE = {
            "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
            "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
            "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
            "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
            "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
            "Z": "--.."
        }

        # fractionated chart
        self.FRACTIONATED = list({
            "A": "...", "B": "..-", "C": "..x", "D": ".-.", "E": ".--", "F": ".-x", "G": ".x.",
            "H": ".x-", "I": ".xx", "J": "-..", "K": "-.-", "L": "-.x", "M": "--.", "N": "---",
            "O": "--x", "P": "-x.", "Q": "-x-", "R": "-xx", "S": "x..", "T": "x.-", "U": "x.x",
            "V": "x-.", "W": "x--", "x": "x-x", "Y": "xx.", "Z": "xx-"
        }.values())

        self.COPRIME_26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        self.COPRIME_INV = [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]


    # turns letters into list of numbers
    def to_numbers(self, plain: str) -> list:
        return [self.ALPHABET.index(letter) for letter in plain]


    # removes all puncutation and spaces (leaves only letters)
    def get_letters(self, plain: str) -> list:
        return [letter for letter in list(plain.upper()) if letter in self.ALPHABET]


    # removes punctuation
    def remove_punctuation(self, plain: str, strip: bool = True) -> str:
        cleaned = plain
        for punc in self.PUNCTUATION:
            cleaned = cleaned.replace(punc, "")
        plain = plain.replace("  ", " ")
        return cleaned
    

    # columnar transposition cipher
    def columnar(self):
        quote, author = random_quote()
        quote = self.remove_punctuation(quote).upper()
        
        words = quote.split(" ")
        crib = random.choice([word for word in words if len(word) > 5])

        # choose number of columns
        max_columns = 9 if len(crib) > 8 else len(crib) + 1
        num_columns = random.randint(4, max_columns)

        # adjust ciphertext 
        quote = self.get_letters(quote)
        remainder = len(quote) % num_columns
        if remainder != 0:
            quote += "X" * (num_columns - remainder)

        # put letters in columns
        columns = ["" for i in range(num_columns)]
        for j in range(len(quote)):
            columns[j % num_columns] += quote[j]

        # shuffle columns
        random.shuffle(columns)

        return f"Solve this Columnar Transposition cipher by {author} that contains the word {crib}.\n{''.join(columns)}\n\n"
    

    # translates text to morse
    def to_morse(self, plain: str) -> str:
        plaintext = self.remove_punctuation(plain).upper()
        morse_text = ""
        for i, char in enumerate(plaintext):
            if char != " ":
                morse_text += self.MORSE[char]
            if i != len(plaintext) - 1:
                morse_text += "x"
        morse_text = morse_text.replace("xxx", "")
        return morse_text


    # fractionated morse cipher
    def fractionated(self):
        plaintext, author = random_quote()
        morse_text = self.to_morse(plaintext)
        
        # adjust length for transcription
        if int(len(morse_text)) % 3 != 0:
            morse_text += "".join(["x" for i in range(3 - (len(morse_text) % 3))])

        # get random word
        rand = random_word().upper()

        # ciphertext alphabet
        cipher_alphabet = rand + "".join([l for l in self.ALPHABET if l not in rand])

        # encryption
        cipher_text = ""
        for j in range(0, len(morse_text), 3):
            triplet = morse_text[j: j + 3]
            letter = cipher_alphabet[self.FRACTIONATED.index(triplet)]
            cipher_text += letter

        question_text = f"Solve this Fractionated Morse cipher by {author} that ends with the word"
        question_text += f"{plaintext[plaintext.rindex(' '):].upper()}\n{'  '.join(cipher_text)}\n\n"

        return question_text

    
    # 2x2 hill cipher
    def hill_2(self):
        plaintext, author = random_quote()
        plaintext = self.get_letters(plaintext)

        # generate key if key not already given
        key = self.hill_key()
        key_text = "".join([self.ALPHABET[k] for k in key])

        # adjust size of plaintext
        plaintext += "Z" if len(plaintext) % 2 == 1 else ""
        
        # get pairs of numbers
        pairings = [(self.ALPHABET.index(plaintext[j]), self.ALPHABET.index(plaintext[j + 1])) for j in range(0, len(plaintext) - 1, 2)]

        # multiply numbers
        cipher_numbers = []
        for pairing in pairings:
            cipher_numbers.append(key[0] * pairing[0] + key[1] * pairing[1])
            cipher_numbers.append(key[2] * pairing[0] + key[3] * pairing[1])

        return f"Decode this Hill Cipher by {author} with the encryption key {key_text}.\n{''.join([self.ALPHABET[number % 26] for number in cipher_numbers])}\n\n"


    # create invertible hill cipher key
    def hill_key(self) -> list:
        rand_key = lambda : [random.randint(0, 25) for i in range(4)]
        key = rand_key()
        while (key[0] * key[3]) - (key[1] * key[2]) not in self.COPRIME_26:
            key = rand_key()
        return key
    

    # 3x3 hill cipher
    def hill_3(self):
        plaintext = self.get_letters("".join([random_word() for i in range(3)]))
        
        # adjust size of plaintext
        remainder = len(plaintext) % 3
        if remainder != 0:
            plaintext += ["Z" for i in range(3 - remainder)]

        # get triplets of numbers - full 3x3 numerial matrices
        triplets = []
        for j in range(0, len(plaintext) - 1, 3):
            triplets.append([self.ALPHABET.index(plaintext[j]), self.ALPHABET.index(plaintext[j + 1]), self.ALPHABET.index(plaintext[j + 2])])

        key, determinant = self.hill_3_key()

        # calculate inverse determinant from determinant
        inverse_determinant = self.COPRIME_INV[self.COPRIME_26.index(determinant)]

        # calculate adjoint matrix
        adjoint = np.zeros_like(key)
        for m in range(3):
            for n in range(3):
                sub_matrix = np.delete(np.delete(key, m, axis=0), n, axis=1)
                adjoint[n, m] = (-1) ** (m + n) * round(np.linalg.det(sub_matrix))
        adjoint = np.mod(adjoint, 26)

        # calculate decryption 
        decryption_key = np.mod(inverse_determinant * adjoint, 26)
        
        # flatten decryption key
        decryption_numbers = list(chain.from_iterable(decryption_key))

        # encrypt plaintext
        encrypted_triplets = []
        for triplet in triplets:
            encrypted_triplets.append(np.dot(key, triplet))
        
        # flatten encrypted numbers
        cipher_numbers = list(chain.from_iterable(encrypted_triplets))

        question_text = "Decode these three words encoded with the Hill Cipher using the decryption key "
        question_text += f"{''.join([self.ALPHABET[number] for number in decryption_numbers])}. \n"
        question_text += f"{''.join([self.ALPHABET[number % 26] for number in cipher_numbers])}\n\n"

        return question_text


    # generates decryptible hill 3x3 key
    def hill_3_key(self):
        rand_key = lambda : [[random.randint(0, 25) for i in range(3)] for j in range(3)]
        key = rand_key()
        determinant = 0
        while determinant not in self.COPRIME_26:
            key = rand_key()
            determinant = round(np.linalg.det(key)) % 26
        return key, determinant


    # finds polybius value for given coordinates
    def polybius_num(self, l: str, table: list) -> int:
        row = 0
        col = 0
        for r in range(5):
            for c in range(5):
                if l in table[r][c]:
                    row = r
                    col = c
        return 10 * (row + 1) + col + 1


    # encrypts plaintext using the Nihilist Cipher
    def nihilist(self):
        plaintext, author = random_quote()
        plaintext = self.get_letters(plaintext)
        
        # generate keywords
        keyword = random_word().upper()
        polyb_key = random_word().upper()

        # create polybius table
        i_index = self.ALPHABET.index("I")
        split_alph = list(self.ALPHABET[: i_index]) + ["IJ"] + list(self.ALPHABET[i_index + 2 :])
        
        # check if I and J are both in the letter
        if "I" in polyb_key and "J" in polyb_key:
            raise Exception("Polybius key cannot be entered into grid.")
        
        polybius_alph = []
        for letter in polyb_key:
            if letter == "I" or letter == "J":
                polybius_alph.append("IJ")
            else:
                polybius_alph.append(letter)

        polybius_alph += [letter for letter in split_alph if letter not in polybius_alph]

        polybius = [list(range(5)) for j in range(5)]
        for j, letter in enumerate(polybius_alph):
            polybius[int(j / 5)][j % 5] = letter
        
        # encrypt cipher
        cipher_numbers = []
        for j, letter in enumerate(plaintext):
            cipher_numbers.append(str(self.polybius_num(keyword[j % len(keyword)], polybius) + self.polybius_num(letter, polybius)))
        
        return f"Solve this Nihilist cipher by {author} with the keyword {keyword} and the Polybius key {polyb_key}.\n{' '.join(cipher_numbers)}\n\n"


    # porta cipher
    def porta(self):
        plaintext, author = random_quote()
        plaintext = self.get_letters(plaintext)
        
        # get keyword
        keyword = random_word(False).upper()
        
        # split alphabet
        first_half = self.ALPHABET[:13]
        second_half = self.ALPHABET[13:]
        
        rows = [second_half[i:] + second_half[:i] for i in range(13)]
        
        # encryption
        ciphertext = ""
        for j, plainLetter in enumerate(plaintext):
            row_index = int(self.ALPHABET.index(keyword[j % len(keyword)]) / 2)
            if plainLetter in first_half:
                ciphertext += rows[row_index][first_half.index(plainLetter)]
            else:
                ciphertext += self.ALPHABET[rows[row_index].index(plainLetter)]
        
        # print question
        return f"Solve this Porta cipher by {author} with the keyword {keyword}.\n{ciphertext}\n\n"


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherGeneratorApp(root)
    root.mainloop()
