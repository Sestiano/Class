# Function 6: Top N Words

from collections import Counter
import re

#Finds the top N most frequent words from a word frequency dictionary.
def top_n_words(text, freq_dict, n):
    words = text.split()
    words = freq_dict.most_common(n)
    return words

#Input:
#- freq_dict (dict): A dictionary where keys are words and values are their frequencies.
#- n (int): The number of top frequent words to return.
text = input('Scrivi qui il testo che vuoi: ')
freq_dict = Counter(re.sub(r'[\.?!:;,./]', "", text.lower()).split())
n = 10

#  Output:
#- list: A list of the top N words in descending order of frequency.

print(top_n_words(text, freq_dict, n))