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

valid_words = {"word": []}

isograms = {
    "word": []
}

sorted_by_length = [{"word" : []} for _ in range(6)]
longer_words = {"word": []}


def is_isogram(word: str) -> bool:
    """ checks if no letters are repeated in word """
    return [word.count(letter) for letter in word] == [1 for n in word]



for i, word in enumerate(raw_words):
    if word.isalpha() and word.islower():
        valid_words["word"].append(word)

        length = len(word)

        if length == 4:
            sorted_by_length[0]["word"].append(word)
        elif length == 5:
            sorted_by_length[1]["word"].append(word)
        elif length == 6:
            sorted_by_length[2]["word"].append(word)
        elif length == 7:
            sorted_by_length[3]["word"].append(word)
        elif length == 8:
            sorted_by_length[4]["word"].append(word)
        elif length == 9:
            sorted_by_length[5]["word"].append(word)
        elif length > 9:
            longer_words["word"].append(word)

        if is_isogram(word):
            isograms["word"].append(word)
        

def write_dict(data: dict, filepath: str):
    """ converst dictionary to DataFrame and writes as CSV """
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)


for i in range(6):
    write_dict(sorted_by_length[i], f"./words/{i + 4}_letters.csv")

write_dict(longer_words, "./words/longer.csv")
write_dict(valid_words, "./words/valid.csv")
write_dict(isograms, "./words/isograms.csv")