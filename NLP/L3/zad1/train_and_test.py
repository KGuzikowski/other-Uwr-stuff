import numpy as np
from numba import njit
from numba.typed import List, Dict
from numba.core import types
import re
import os
from sklearn.model_selection import train_test_split
from model import AutocorrectModel, lower_in_array


@njit
def analize_sentence_for_unigram(unigram, sentence):
    for j in range(len(sentence)):
        if sentence[j] in unigram:
            unigram[sentence[j]] += 1
        else:
            unigram[sentence[j]] = 2
    return unigram


def create_unigram(data: np.ndarray):
    unigram = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.int32,
    )
    for sentence in data:
        unigram = analize_sentence_for_unigram(unigram, sentence)
    return unigram


@njit
def analize_sentence_for_bigram(bigram, sentence):
    for i in range(len(sentence) - 1):
        if sentence[i] + '`|;' + sentence[i + 1] in bigram:
            bigram[sentence[i] + '`|;' + sentence[i + 1]] += 1
        else:
            bigram[sentence[i] + '`|;' + sentence[i + 1]] = 2
    return bigram


def create_bigram(data: np.ndarray):
    bigram = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.int32,
    )
    for sentence in data:
        bigram = analize_sentence_for_bigram(bigram, sentence)
    return bigram


def save_unigram(unigram):
    with open('./unigram.txt', 'w') as file:
        for word, qty in unigram.items():
            file.write(f'{qty} {word}\n')
    command1 = 'sort -nr unigram.txt > train_unigram.txt'
    command2 = 'rm unigram.txt'
    os.system(command1)
    os.system(command2)


def save_bigram(bigram):
    with open('./bigram.txt', 'w') as file:
        for words, qty in bigram.items():
            words = words.split('`|;')
            file.write(f'{qty} {words[0]} {words[1]}\n')
    command1 = 'sort -nr bigram.txt > train_bigram.txt'
    command2 = 'rm bigram.txt'
    os.system(command1)
    os.system(command2)


# import and tokenize data
corpus = List()
with open('./limited.txt') as file:
    for line in file:
        l = List()
        splitted = line.strip().split()
        for elem in splitted:
            l.append(elem)
        corpus.append(l)

corpus = np.array(corpus, dtype=object)

train, test = train_test_split(corpus, test_size=0.1, shuffle=False)

for i in range(train.shape[0]):
    train[i] = lower_in_array(train[i])

dir_content = os.listdir()
if 'train_unigram.txt' not in dir_content:
    save_unigram(create_unigram(train))
if 'train_bigram.txt' not in dir_content:
    save_bigram(create_bigram(train))

model = AutocorrectModel(train)
model.test(test)
