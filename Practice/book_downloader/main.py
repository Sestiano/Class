from cleaning import clean_text, split_text, read_book, download_book

# read the list of books from the booklist.txt

with open('Intro-to-Python-Exercises/book_downloader/booklist.txt', 'r') as f:
    books = f.readlines()

# split the books into name and urls, comma separated
books = [i.strip().split(',') for i in books]

# Process the books

for book in books:
    # remove spaces from the book name
    book[0] = book[0].replace(' ', '_')
    tmp_book = download_book(book[1], path=f'{book[0]}.txt')
    tmp_book = read_book(file_path=f'{book[0]}.txt')
    tmp_book = clean_text(tmp_book)
    sentences = split_text(tmp_book)
    for i in sentences[100:110]:
        print(i)
    print('------------------------------------')
