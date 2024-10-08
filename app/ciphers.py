"""
Andrew Kim

8 October 2024

Version `0.0.1`

Cipher generator class
"""



import random
import numpy as np
from itertools import chain


class Ciphers:
    def __init__(self):
        # alphabet
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # punctuation characters
        self.PUNCTUATION = '''!()-[]{};:'",<>./?@#$%^&*_~'''

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
    def columnar(self, random_quote: tuple) -> tuple:
        quote, author = random_quote
        quote = self.remove_punctuation(quote).upper()
        
        try:
            words = quote.split(" ")
            crib = random.choice([word for word in words if len(word) > 5])
        except:
            return ("", "")

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

        return f"Solve this Columnar Transposition cipher by {author} that contains the word {crib}.", ''.join(columns)
    

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
    def fractionated(self, random_quote: tuple, random_word: str) -> tuple:
        plaintext, author = random_quote
        morse_text = self.to_morse(plaintext)
        
        # adjust length for transcription
        if int(len(morse_text)) % 3 != 0:
            morse_text += "".join(["x" for i in range(3 - (len(morse_text) % 3))])

        # get random word
        rand = random_word.upper()

        # ciphertext alphabet
        cipher_alphabet = rand + "".join([l for l in self.ALPHABET if l not in rand])

        # encryption
        cipher_text = ""
        for j in range(0, len(morse_text), 3):
            triplet = morse_text[j: j + 3]
            letter = cipher_alphabet[self.FRACTIONATED.index(triplet)]
            cipher_text += letter

        return f"Solve this Fractionated Morse cipher by {author} that ends with the word {plaintext[plaintext.rindex(' '):].upper()}", '  '.join(cipher_text)

    
    # 2x2 hill cipher
    def hill_2(self, random_quote: tuple) -> tuple:
        plaintext, author = random_quote
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

        return f"Decode this Hill Cipher by {author} with the encryption key {key_text}.", ''.join([self.ALPHABET[number % 26] for number in cipher_numbers])


    # create invertible hill cipher key
    def hill_key(self) -> list:
        rand_key = lambda : [random.randint(0, 25) for i in range(4)]
        key = rand_key()
        while (key[0] * key[3]) - (key[1] * key[2]) not in self.COPRIME_26:
            key = rand_key()
        return key
    

    # 3x3 hill cipher
    def hill_3(self, word_1: str, word_2: str, word_3: str) -> tuple:
        plaintext = self.get_letters(word_1 + word_2 + word_3)
        
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
        question_text += f"{''.join([self.ALPHABET[number] for number in decryption_numbers])}."

        return question_text, f"{''.join([self.ALPHABET[number % 26] for number in cipher_numbers])}"


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
    def nihilist(self, random_quote: tuple, key: str, polyb: str) -> tuple:
        plaintext, author = random_quote
        plaintext = self.get_letters(plaintext)

        keyword = key.upper()
        polybius = polyb.upper()
        
        # create polybius table
        i_index = self.ALPHABET.index("I")
        split_alph = list(self.ALPHABET[: i_index]) + ["IJ"] + list(self.ALPHABET[i_index + 2 :])
        
        # check if I and J are both in the letter
        if "I" in polybius and "J" in polybius:
            raise Exception("Polybius key cannot be entered into grid.")
        
        polybius_alph = []
        for letter in polybius:
            temp_letter = None
            if letter == "I" or letter == "J":
                temp_letter = "IJ"
            else:
                temp_letter = letter
            if temp_letter not in polybius_alph:
                polybius_alph.append(temp_letter)

        polybius_alph += [letter for letter in split_alph if letter not in polybius_alph]
        polybius_table = [list(range(5)) for j in range(5)]
        for j, letter in enumerate(polybius_alph):
            polybius_table[int(j / 5)][j % 5] = letter
        
        # encrypt cipher
        cipher_numbers = []
        for j, letter in enumerate(plaintext):
            cipher_numbers.append(str(self.polybius_num(keyword[j % len(keyword)], polybius_table) + self.polybius_num(letter, polybius_table)))
        
        return f"Solve this Nihilist cipher by {author} with the keyword {keyword} and the Polybius key {polybius}", ' '.join(cipher_numbers)


    # porta cipher
    def porta(self, random_quote: tuple, random_word: str) -> tuple:
        plaintext, author = random_quote
        plaintext = self.get_letters(plaintext)
        
        # get keyword
        keyword = random_word.upper()
        
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
        
        # return f"Solve this Porta cipher by {author} with the keyword {keyword}.\n{ciphertext}\n\n"
        return f"Solve this Porta cipher by {author} with the keyword {keyword}", ciphertext
