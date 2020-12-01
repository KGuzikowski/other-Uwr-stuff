import re
import collections
from typing import Dict, List, Tuple, Optional
from math import log
from operator import itemgetter
import random

SYLLABLES_NO = 13  # number of syllables
LINES_NO = 2  # number of lines
VOWELS = 'aąeęiouy'
words_qty = {}
FORBIDDEN = ['<BOS>', '<EOS>']
corpus_size = 0

X = 10000000  # I'll be working on sorted bigram of only X elements
PAN_TADEUSZ_SAMPLE_TAGS: List[List[str]] = []
unigram: Dict[str, int] = collections.OrderedDict()
bigram: Dict[Tuple[str, str], int] = collections.OrderedDict()
poem: List[List[str]] = []  # list of lists - each inner list is a line of poem
tags: Dict[str, str] = {}

with open('./unigram.txt', encoding='utf-8') as file:
    for line in file:
        qty, word = line.split()
        if re.match('[^a-ząćęłńóśźż]+', word):
            continue
        qty = int(qty)
        corpus_size += qty
        qty += 1
        unigram[word] = qty

with open('../poleval_2grams.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i < X:
            qty, a, b = line.split()
            if re.match('[^a-ząćęłńóśźż]+', a) or re.match('[^a-ząćęłńóśźż ]+', b):
                continue
            qty = int(qty) + 1
            bigram[(a, b)] = qty

with open('./supertags.txt', encoding='utf-8') as file:
    for line in file:
        word, tag = line.split()
        tags[word] = tag


with open('./pan_tadeusz_tags.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split()
        PAN_TADEUSZ_SAMPLE_TAGS.append(data)


def count_syllables(text: str) -> int:
    number = 0
    text = text.split()
    for word in text:
        if len(word) == 1:
            number += 1
            continue
        i = 0
        while i < len(word):
            if word[i] in VOWELS:
                j = 1
                while i + j < len(word) and word[i + j] in VOWELS:
                    j += 1
                number += 1
                i += j
            else:
                i += 1
    return number


def get_word_ending(word: str) -> str:
    i = len(word) - 1
    preceding_consonant = False
    while i >= 0:
        if word[i] in VOWELS:
            if preceding_consonant:
                return word[i:]
        else:
            preceding_consonant = True
        i -= 1
    return word


def get_word_ending_longer(word: str) -> str:
    i = len(word) - 1
    preceding_consonant = False
    first_found = False
    while i >= 0:
        if word[i] in VOWELS:
            if preceding_consonant and first_found:
                return word[i:]
            first_found = True
        else:
            preceding_consonant = True
        i -= 1
    return word


def already_found(rhymes: List[List[str]], new_one: str) -> bool:
    for rhyme in rhymes:
        if len(rhyme) == 2 and rhyme[1] == new_one:
            return True
    return False


def get_unigram_rhymes(word: str, number: int, word_ending: str, word_syllables_no: int, rhymes_in_use=None) -> List[List[str]]:
    if rhymes_in_use is None:
        rhymes_in_use = []
    rhymes = []
    for unigram_elem in unigram.keys():
        if (unigram_elem != word and
                get_word_ending(unigram_elem) == word_ending and
                count_syllables(unigram_elem) == word_syllables_no):
            if len(unigram_elem) <= 3 or already_found(rhymes_in_use + rhymes, unigram_elem):
                continue
            rhymes.append([unigram_elem])
            number -= 1
            if number == 0:
                return rhymes
    return rhymes


def get_bigram_rhymes(word: str, number: int, word_ending: str, word_syllables_no: int) -> List[List[str]]:
    rhymes = []
    for bigram_elem, qty in bigram.items():
        a, b = bigram_elem
        if (b != word and
                get_word_ending(b) == word_ending and
                count_syllables(b) == word_syllables_no):
            if len(b) <= 3 or already_found(rhymes, b):
                continue
            rhymes.append([a, b])
            number -= 1
            if number == 0:
                return rhymes
    return rhymes


# We'll first look at most frequent bigrams and then on most frequent unigrams.
def get_rhymes_for(word: str, number: int, word_ending_func: any) -> List[List[str]]:
    word_syllables_no = count_syllables(word)
    word_ending = word_ending_func(word)
    bigram_rhymes = get_bigram_rhymes(word, number, word_ending, word_syllables_no)
    unigram_rhymes = get_unigram_rhymes(word, number, word_ending, word_syllables_no, bigram_rhymes)
    return bigram_rhymes + unigram_rhymes


def calculate_psm(x: str, y: str) -> Tuple[str, float]:
    c_x = unigram[x] if x in unigram else 1
    c_y = unigram[y] if y in unigram else 1
    f_xy = qty
    g_xy = (c_x * c_y) / corpus_size
    psm_one = f_xy * (log(f_xy) - log(g_xy) - 1)
    return (y, psm_one)


# Function calculates Poisson-Stirling Approximation and uses it to choose the best word.
def choose_best_following_word(word: str, line_so_far=None, how_many_to_return: int = 1, reverse: bool = False) -> List[Tuple[str, float]]:
    if line_so_far is None:
        line_so_far = []
    psm = []
    for bigram_elem, qty in bigram.items():
        if word not in bigram_elem:
            continue
        candidate: str
        if reverse:
            if bigram_elem[0] == word:
                continue
            candidate = bigram_elem[0]
            # print('reverse true - line_so_far', line_so_far)
        else:
            if bigram_elem[1] == word:
                continue
            # print('reverse false - line_so_far', line_so_far)
            candidate = bigram_elem[1]
        if len(candidate) >= 2 and candidate not in FORBIDDEN:
            # Poisson-Stirling Approximation
            psm.append(calculate_psm(word, candidate))

    psm.sort(key=itemgetter(1), reverse=True)
    if how_many_to_return > len(psm):
        return psm
    return psm[:how_many_to_return]


def check_text(text: List[str]) -> bool:
    text_tags = []
    for word in text:
        if word in tags:
            text_tags.append(tags[word])
        else:
            return False

    for sentence_tags in PAN_TADEUSZ_SAMPLE_TAGS:
        if len(text) > len(sentence_tags):
            continue
        diff = len(sentence_tags) - len(sentence_tags) + 1
        for i in range(diff):
            if text_tags == sentence_tags[i:i+len(text_tags)]:
                return True
    return False


def generate_sentence(line: List[str] = None, curr_syllables_no: int = 0, verbose: bool = False, reverse: bool = False) -> Optional[List[str]]:
    if line is None:
        line = []
    if curr_syllables_no > SYLLABLES_NO:
        return None
    if len(line) == 0:
        for _ in range(100):
            word = random.choice(list(bigram.keys()))[0]
            line.append(word)
            curr_syllables_no = count_syllables(' '.join(line))
            if curr_syllables_no == SYLLABLES_NO:
                return line
            result = generate_sentence(line=line.copy(), curr_syllables_no=curr_syllables_no, reverse=reverse)
            if result:
                return result
    else:
        prev = line[-1]
        next_words_candidates: List[Tuple[str, float]] = choose_best_following_word(prev, line_so_far=line, how_many_to_return=20, reverse=reverse)
        for candidate in next_words_candidates:
            line_with_next_word_syllables_no = count_syllables(' '.join(line + [candidate[0]]))
            if line_with_next_word_syllables_no > SYLLABLES_NO:
                return None
            curr_line = line.copy()
            check_all = check_text([candidate[0]] + curr_line) if reverse else check_text(curr_line + [candidate[0]])
            if not check_all:
                continue
            if verbose:
                print('check_text is true!')
            if reverse:
                curr_line = [candidate[0]] + curr_line
            else:
                curr_line.append(candidate[0])
            curr_syllables_no_local = line_with_next_word_syllables_no
            if curr_syllables_no_local == SYLLABLES_NO:
                return curr_line
            result = generate_sentence(line=curr_line, curr_syllables_no=curr_syllables_no_local, reverse=reverse)
            if result:
                if verbose:
                    print('prev', prev)
                    print('next_words_candidates', next_words_candidates)
                return result
    return None


for _ in range(20):
    i = 1
    j = 0
    while i <= LINES_NO:
        j += 1
        # first line or odd numbered line
        if i % 2 != 0:
            line = generate_sentence()
            if not line:
                # lets backtrack
                if i == 1:
                    i = 1
                else:
                    i -= 1
                poem = poem[:-1]
                continue
            else:
                # print(' '.join(line), count_syllables(' '.join(line)))
                poem.append(line)
        else:
            # here we need to generate a rhyme and then go backwords creating a sentence
            # print('Ending of prev line', poem[i-2][-1])
            prev_word = poem[i - 2][-1]
            word_ending_func = get_word_ending_longer if count_syllables(prev_word) >= 2 else get_word_ending
            rhymes = get_rhymes_for(prev_word, 5, word_ending_func)
            # print('Possible rhymes', rhymes)
            works = False
            line = None
            for rhyme in rhymes:
                if j > 20:
                    break
                line = generate_sentence(line=rhyme.copy(), reverse=True)
                if line:
                    works = True
                    break
            if not works:
                # lets backtrack
                i -= 1
                poem = poem[:-1]
                continue
            else:
                # print(' '.join(line), count_syllables(' '.join(line)))
                poem.append(line)
        i += 1

    with open('./poems.txt', 'a') as file:
        for line in poem:
            sentence = ' '.join(line)
            file.write(sentence + '\n')
        file.write('\n')
        file.write('-' * 20 + '\n')
        file.write('\n')
