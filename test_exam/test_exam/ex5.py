import re
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


text = input('Scrivi qua il testo con le parole da contare: ')
print(word_frequencies(text))
    
    