import re

def word_count(text):
    text = re.sub(r'[\.?!:;,./]', '', text)
    words = text.split()
    return len(words)

text = input('Scrivi qua il testo con le parole da contare: ')
print(word_count(text))