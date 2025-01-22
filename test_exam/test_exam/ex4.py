# Function 4: Unique Word Count

import re
#Counts the number of unique words in a given text.
def unique_word_count(text):
    text = re.sub(r'[\.?!:;,./]', '', text)
    words = text.split()
    uniquewords = {}
    for word in words:
        if word not in uniquewords:
            uniquewords[word] = 1
    return len(uniquewords)


#Input:
#- text (str): A cleaned text string with words separated by whitespace.
text = input('Scrivi qua il testo con le parole da contare: ')

#Output:
#- int: Number of unique words in the text.
print(unique_word_count(text))