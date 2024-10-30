from collections import Counter

def top_n_words(freq_dict, n):
    words = [(word, count) for word, count in freq_dict.most_common(n)]
    return words

text = input('Scrivi qui il testo che vuoi: ')
words = text.lower().split()
freq_dict = Counter(words)
n = 10
print(top_n_words(freq_dict, n))