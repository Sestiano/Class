import re

def clean_text(text):
    text = text.lower()
    text = re.split(r'[\.?!:;,./]', text)
    return text
    
text = input('Scrivi il testo da pulire:')
print(clean_text(text))