import re

def read_text_file(filepath):
    with open(filepath) as f:
        book = f.read()
    return book


book = read_text_file('/home/seb/develop/Class/test_exam/test_exam/data/Frankenstein.txt')
print(book)