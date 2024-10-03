"""
Andrew Kim

2 October 2024

Version `0.0.1`

Preprocess quote data
"""

# import external libraries
import pandas as pd


QUOTE_PATH = "./data/quotes.csv"


def read_csv(filepath: str) -> list:
    """ reads quotes from csv file and returns """