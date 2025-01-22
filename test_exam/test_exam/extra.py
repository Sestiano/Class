import re
import os
from collections import Counter

# read all text in files
def read_all(data):
    content = ""
    for filename in os.listdir(data):
        filepath = os.path.join(data, filename)
        if os.path.isfile(filepath) and filename.endswith(".txt"):  # Check if it's a .txt file
            with open(filepath, 'r', encoding='utf-8') as f:
                content += f.read() + " "
    return content

# word frequencies 
def word_frequencies(text, n):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()  # Split by whitespace
    freq_dict = Counter(words)  # Count word frequencies
    most_common_words = freq_dict.most_common(n)  # Get 'n' most common words
    return most_common_words

# Set parameters
data_directory = "/home/seb/develop/Class/test_exam/test_exam/data"
n = 10  # Number of most frequent words to display

# Get all text and calculate frequencies
frequencies = word_frequencies(read_all(data_directory), n)

# Print the most frequent words
for word, freq in frequencies:
    print(f"{word}: {freq}")