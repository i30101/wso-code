"""
Andrew Kim

2 October 2024

Version `0.0.1`

Preprocess quote data
"""

# import external libraries
import pandas as pd


RAW_QUOTE_PATH = "./data/quotes.csv"
QUOTE_PATH = "./quotes/quotes.csv"



def read_csv(read_path: str, write_path: str) -> list:
    """ reads quotes from csv file and returns """
    df = pd.read_csv(read_path)
    quote_dict = {
        "quote": [],
        "author": []
    }
    for row in df.itertuples():
        quote = row[1]
        raw_author = row[2]

        if isinstance(quote, float) or isinstance(raw_author, float):
            continue

        print(quote)
        if "\"" in quote:
            quote.replace("\"", "")

        if type(raw_author) != float:
            if "," in raw_author:
                author = raw_author[:raw_author.index(",")]
            else:
                author = raw_author
            quote_dict["quote"].append(quote)
            quote_dict["author"].append(author)
    quote_df = pd.DataFrame(quote_dict)
    quote_df.to_csv(write_path)


        

read_csv(RAW_QUOTE_PATH, QUOTE_PATH)