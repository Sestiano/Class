import re

def read_text_file(filepath):
    with open(filepath) as f:
        book = f.read()
    return book


book = read_text_file('data/Frankenstein.txt')
print(book)