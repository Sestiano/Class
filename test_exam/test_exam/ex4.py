import re
def unique_word_count(text):
    text = re.sub(r'[\.?!:;,./]', '', text)
    words = text.split()
    uniquewords = {}
    for word in words:
        if word not in uniquewords:
            uniquewords[word] = 1
    return len(uniquewords)

text = input('Scrivi qua il testo con le parole da contare: ')
print(unique_word_count(text))
