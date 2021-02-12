import numpy as np
from numba import njit
from numba.typed import Dict, List
from numba.core import types
import re

# I will naively assume that a word after '.' should start with uppercase letter


def read_unigram():
    unigram = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.int32,
    )
    with open('./train_unigram.txt') as file:
        for line in file:
            line = line.split()
            unigram[line[1]] = int(line[0])
    return unigram


def read_bigram():
    bigram = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.int32,
    )
    with open('./train_bigram.txt') as file:
        for line in file:
            line = line.split()
            bigram[f'{line[1]}`|;{line[2]}'] = int(line[0])
    return bigram


@njit
def get_corpus_size(unigram):
    num = 0
    for qty in unigram.values():
        num += qty
    return num


@njit
def get_prob(qty, N):
    return qty / N


@njit
def break_word(text):
    new_text = ''
    for i in range(len(text)):
        if text[i] == 'ą':
            new_text += 'a'
        elif text[i] == 'ć':
            new_text += 'c'
        elif text[i] == 'ę':
            new_text += 'e'
        elif text[i] == 'ł':
            new_text += 'l'
        elif text[i] == 'ń':
            new_text += 'n'
        elif text[i] == 'ó':
            new_text += 'o'
        elif text[i] == 'ś':
            new_text += 's'
        elif text[i] == 'ż':
            new_text += 'z'
        elif text[i] == 'ź':
            new_text += 'z'
        else:
            new_text += text[i]
    return new_text


@njit
def levenshtein_distance(x, y):
    # for all i and j, d[i,j] will hold the Levenshtein distance between
    # the first i characters of x and the first j characters of y
    d = np.zeros((len(x), len(y)))
    # source prefixes can be tansformed into
    # empty string by dropping all characters
    for i in range(len(x)):
        d[i, 0] = i
    # target prefixes can be reached from empty
    # source prefix by inserting every character
    for j in range(len(y)):
        d[0, j] = j
    for j in range(len(y)):
        for i in range(len(x)):
            if x[i] == y[j]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            d[i, j] = min(d[i - 1, j] + 1,  # deletion
                          d[i, j - 1] + 1,  # insertion
                          d[i - 1, j - 1] + substitution_cost)  # substitution
    return int(d[len(x)-1, len(y)-1])


@njit
def split_bigram(bigram):
    for i in range(len(bigram)):
        if bigram[i:i+3] == '`|;':
            return bigram[:i], bigram[i+3:]
    return '', ''


@njit
def get_new_best(observation, word, unigram, qty, N, max_val, best, bigram=True):
    word_dist = levenshtein_distance(observation, word)
    if word_dist <= :
        pb = (np.log(unigram[word]) - np.log(word_dist)) + (np.log(qty) - np.log(N))
        if bigram:
            pb *= 3
        if pb > max_val:
            max_val = pb
            best = word
    return max_val, best


@njit
def fix(observations, unigram, bigram, N):
    solution = List()
    for i in range(len(observations)):
        max_val = -1
        best = ''
        for bigram_elem, qty in bigram.items():
            if i == len(observations) - 1:
                _, word = split_bigram(bigram_elem)
            else:
                word, _ = split_bigram(bigram_elem)
            # print(observations)
            # print(i, observations[i], bigram_elem)
            max_val, best = get_new_best(observations[i], word, unigram, qty, N, max_val, best)
        if max_val != -1:
            solution.append(best)
            continue
        max_val = -1
        best = ''
        for word, qty in unigram.items():
            max_val, best = get_new_best(observations[i], word, unigram, qty, N, max_val, best, False)
        if max_val != -1:
            solution.append(best)
    return solution


@njit
def lower_in_array(arr):
    for i in range(len(arr)):
        arr[i] = arr[i].lower()
    return arr


class AutocorrectModel(object):
    def __init__(self, train_data):
        """
        Warning:
        Due to the fact that the train set will be very large
        I will compute a_ij, pi_i and b_i(o_k) on the fly.
        b_i(o_k) will be calculated as a Levenshtein distance.
        """
        self.bigram = read_bigram()
        self.unigram = read_unigram()
        self.N = get_corpus_size(self.unigram)

    def test(self, test_set):
        for i, elem in enumerate(test_set):
            if i == 2:
                break
            good_sentence = lower_in_array(elem)
            bad_sentence = [break_word(elem) for elem in good_sentence]
            print('good_sentence:', good_sentence)
            print('bad sentence:', bad_sentence)
            solution = self.fix(bad_sentence)
            print('solution', solution)
            print('+'*30)

    def fix(self, observations):
        return fix(observations, self.unigram, self.bigram, self.N)
