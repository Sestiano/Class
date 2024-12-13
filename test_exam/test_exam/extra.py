"""
Exercise: Word Frequency Analysis from Multiple Text Files

Write a Python program that reads all text files in `data/`, combines the contents of these files, and performs a frequency analysis on the words. The program should output the most common words and their frequencies ordered from the highest to the lowest

"""

import os
import re
from collections import Counter
import matplotlib.pyplot as plt

def read_data(directory):
    combined_data = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath) as f:
                combined_data += f.read() + " "
    return combined_data

def word_frequency_analysis(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

data_directory = '/home/seb/develop/Class/test_exam/test_exam/data'
data = read_data(data_directory)
word_frequencies = word_frequency_analysis(data)

for word, freq in word_frequencies.most_common():
    print(f"{word}: {freq}")
    # Output the most common words and their frequencies
    for word, freq in word_frequencies.most_common():
        print(f"{word}: {freq}")
    # Output the most common words and their frequencies
        for word, freq in word_frequencies.most_common(10):
            print(f"{word}: {freq}")

    # Generate a bar graph for the top 10 most common words and save it as a PNG file
    top_words = word_frequencies.most_common(10)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequencies')
    plt.title('Top 10 Most Common Words')
    plt.savefig('/home/seb/develop/Class/test_exam/test_exam/top_words.png')
    plt.show()