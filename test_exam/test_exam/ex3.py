# Function 3: Word Count

import re

# Counts the total number of words in a given text.
def word_count(text):
    text = re.sub(r'[\.?!:;,./]', '', text)
    words = text.split()
    return len(words)

#Input:
#- text (str): A cleaned text string with words separated by whitespace.
text = input('Scrivi qua il testo con le parole da contare: ')  
#Output:
#- int: Total number of words in the text.
print(word_count(text))