# Function 2: Clean Text
import re


#Cleans a text string by removing punctuation and converting all characters to lowercase.
def clean_text(text):
    text = text.lower()
    text = re.split(r'[\.?!:;,./]',text)
    return text
    
#Input:
#- text (str): The original text string.
text = input("scrivi il testo da pulire: ")
#Output:
#- str: The cleaned text with no punctuation and all lowercase characters.
print(clean_text(text))