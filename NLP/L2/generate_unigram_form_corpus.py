import re
import os

unigram = {}

with open('../polish_corpora.txt', encoding='utf-8') as file:
    for line in file:
        data = line.lower().split()
        for word in data:
            if word in unigram:
                unigram[word] += 1
            else:
                unigram[word] = 1

with open('./unigram_unsorted.txt', "w") as file:
    for word, qty in unigram.items():
        file.write(f'{qty} {word}\n')

command1 = 'sort -nr unigram_unsorted.txt > unigram.txt'
command2 = 'rm unigram_unsorted.txt'
os.system(command1)
os.system(command2)
