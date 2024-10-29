import re
import requests
import os

def clean_text(text):
    text = re.sub('[\n\t]', '', text)
    text = re.sub(' +', ' ', text)
    return text

def split_text(text):
    sentences = re.split("[\.\?!;:]", text)
    sentences = [i.strip() for i in sentences if i.strip()!='']
    return sentences

def read_book(file_path):
    with open(file_path,'r') as f:
        book = f.read()
    return book

def download_book(url, path='book.txt'):
    r = requests.get(url)
    # Save the book to a file
    with open(path, 'w') as f:
        f.write(r.text)
    return r.text


if __name__ == '__main__':
    url = 'https://www.gutenberg.org/files/84/84-0.txt'
    filepath = 'bookcode/Frankenstein.txt'
    book = download_book(url, path=filepath)
    book = read_book(file_path=filepath)
    book = clean_text(book)
    sentences = split_text(book)
    for i in sentences[100:110]:
        print(i)
