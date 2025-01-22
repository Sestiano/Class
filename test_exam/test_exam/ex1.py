# Function 1: Read Text File
#import regex library
import re

#Reads the content of a text file.
def read_text_file(filepath):
    with open(filepath) as f:
        book = f.read()
    return book  

#Input:
#- filepath (str): Path to the text file to be read.
book = read_text_file(input("copy and paste the filepath of the book you want to read: "))
        
#Output:
#- str: The entire text content of the file as a single string.
print(book)