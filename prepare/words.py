"""
Andrew Kim

2 October 2024

Version `0.0.1`

Preprocess word data
"""


# import external libraries
import pandas as pd


WORD_TXT_PATH = "./data/words.txt"
WORD_CSV_PATH = "./data/words.csv"


def read_txt(filepath: str) -> list:
    """ reads text file and returns contents as list"""
    file = open(filepath, "r")
    words = [word.replace("\n", "") for word in file]
    return words


def write_txt(filepath: str, data: list):
    with open(filepath, 'w') as f:
        f.write("\n".join(data))


def read_csv(filepath: str) -> list:
    """ reads csv file and returns column as list"""
    raw = pd.read_csv(filepath)
    return raw['word'].tolist()



# raw_words = read_txt(WORD_TXT_PATH)
raw_words = read_csv(WORD_CSV_PATH)[:10000]

valid_words = []

sorted_by_length = [[] for _ in range(6)]
longer_words = []

for i, word in enumerate(raw_words):
    if word.isalpha() and word.islower():
        valid_words.append(word)

        length = len(word)

        if length == 4:
            sorted_by_length[0].append(word)
        elif length == 5:
            sorted_by_length[1].append(word)
        elif length == 6:
            sorted_by_length[2].append(word)
        elif length == 7:
            sorted_by_length[3].append(word)
        elif length == 8:
            sorted_by_length[4].append(word)
        elif length == 9:
            sorted_by_length[5].append(word)
        elif length > 9:
            longer_words.append(word)

for i in range(6):
    write_txt(f"./words/{i + 4}_letters.txt", sorted_by_length[i])
write_txt("./words/longer_words.txt", longer_words)


write_txt("./words/valid.txt", valid_words)
