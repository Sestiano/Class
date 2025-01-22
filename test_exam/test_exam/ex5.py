# Function 5: Word Frequencies
import re

#Generates a dictionary with word frequencies.
def word_frequencies(text):
    text = re.sub(r'[\.?!:;,./]', '', text)
    words = text.split()
    unique = {}
    for word in words:
        if word not in unique:
            unique[word] = 1
        else:
            unique[word] += 1
    return unique

#Input:
#- text (str): A cleaned text string with words separated by whitespace.     
text = input('Scrivi qua il testo con le parole da contare: ')

#Output:
#- dict: A dictionary where keys are words and values are the frequencies of each word.
print(word_frequencies(text))
    
    