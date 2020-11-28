from math import log, exp
from operator import itemgetter

K = 10
WORDS = ['kolej', 'uczelnia', 'teren', 'auto', 'malarz', 'ziemia', 'komputer', 'budowa', 'polak', 'słońce']
TAGS = {}
WORDS_QTY = {}
TAGS_QTY = {}
all_tags = 0
collocations = {}
bigram = {}
forbidden = ['<BOS>', '<EOS>']
alpha = 0.75
all_words_qty_with_alpha_sum = 0
corpus_size = 0
bigrams_qty = 0

for word in WORDS:
    collocations[word] = []
    bigram[word] = []

with open('./data_for_task_5.txt', encoding='utf-8') as file:
    for line in file:
        for word in WORDS:
            if word in line:
                qty = int(line.split()[0]) + 1
                corpus_size += qty
                WORDS_QTY[word] = qty
                all_words_qty_with_alpha_sum += qty ** alpha


with open('../poleval_2grams.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split()
        bigrams_qty += 1
        for word in WORDS:
            if word in data:
                data[0] = int(data[0])
                bigram[word].append(data)

with open('./supertags.txt', encoding='utf-8') as file:
    for line in file:
        data = line.split()
        all_tags += 1
        TAGS[data[0]] = data[1]
        if data[1] in TAGS:
            TAGS_QTY[data[1]] += 1
        else:
            TAGS_QTY[data[1]] = 2

PPMI = {}
PSM = {}
GRAMMATICAL_AND_WORD = {}
CM = {}
CM2 = {}


def calculate_word_prob(word, alpha=alpha):
    a = WORDS_QTY[word] ** alpha if word in WORDS_QTY else 1
    return a / all_words_qty_with_alpha_sum


def is_the_same_tag(word, x):
    if word in TAGS and x in TAGS and TAGS[word] == TAGS[x]:
        return 50
    return 0


for word in WORDS:
    PPMI[word] = []
    PSM[word] = []
    GRAMMATICAL_AND_WORD[word] = []
    CM[word] = []
    CM2[word] = []
    data = sorted(bigram[word], key=itemgetter(0), reverse=True)
    for bigram_elem in data:
        candidate = bigram_elem[2] if word == bigram_elem[1] else bigram_elem[1]
        if len(candidate) > 3 and candidate not in forbidden:
            # PPMI
            p_w1 = calculate_word_prob(bigram_elem[1])
            p_w2 = calculate_word_prob(bigram_elem[2])
            pmi = max(
                0,
                log((bigram_elem[0] + 1) / ((WORDS_QTY[bigram_elem[1]] if bigram_elem[1] in WORDS_QTY else 1) * p_w1 * p_w2))
            )

            # Poisson-Stirling Approximation
            c_x = WORDS_QTY[bigram_elem[1]] if bigram_elem[1] in WORDS_QTY else 1
            c_y = WORDS_QTY[bigram_elem[2]] if bigram_elem[2] in WORDS_QTY else 1
            f_xy = bigram_elem[0]
            g_xy = (c_x * c_y) / corpus_size
            psm_one = f_xy * (log(f_xy) - log(g_xy) - 1)

            # Grammatical and word collocations by using simple propability
            for_words = log(bigram_elem[0]) - log(bigrams_qty)
            first_tag = TAGS_QTY[TAGS[bigram_elem[1]]] if bigram_elem[1] in TAGS else 1
            second_tag = TAGS_QTY[TAGS[bigram_elem[2]]] if bigram_elem[2] in TAGS else 1
            for_tags = log(first_tag) + log(second_tag) - log(all_tags)
            g_a_w = exp(for_words) + exp(for_tags)

            """
            My own idea:
            f(xy) - qty of bigram
            f2(xy) - estimated qty of bigram:
                f2(xy) = cnt(x) * cnt(x) / N
            cm - collocation metric
            cm = f/f2
            """
            f = bigram_elem[0]
            cnt_x = WORDS_QTY[bigram_elem[1]] if bigram_elem[1] in WORDS_QTY else 1
            cnt_y = WORDS_QTY[bigram_elem[2]] if bigram_elem[2] in WORDS_QTY else 1
            f2 = (c_x * c_y) / corpus_size
            cm = f / f2

            if word == bigram_elem[1]:
                bonus_pionts = is_the_same_tag(word, bigram_elem[2])
                pmi += bonus_pionts
                psm_one += bonus_pionts
                PPMI[word].append((bigram_elem[2], pmi))
                PSM[word].append((bigram_elem[2], psm_one))
                GRAMMATICAL_AND_WORD[word].append((bigram_elem[2], g_a_w))
                CM[word].append((bigram_elem[2], cm))
                CM2[word].append((bigram_elem[2], cm + bonus_pionts))
            else:
                bonus_pionts = is_the_same_tag(word, bigram_elem[1])
                pmi += bonus_pionts
                psm_one += bonus_pionts
                PPMI[word].append((bigram_elem[1], pmi))
                PSM[word].append((bigram_elem[1], psm_one))
                GRAMMATICAL_AND_WORD[word].append((bigram_elem[1], g_a_w))
                CM[word].append((bigram_elem[1], cm))
                CM2[word].append((bigram_elem[1], cm + bonus_pionts))


for word in WORDS:
    ppmi_data = sorted(PPMI[word], key=itemgetter(1), reverse=True)
    psm_data = sorted(PSM[word], key=itemgetter(1), reverse=True)
    gaw_data = sorted(GRAMMATICAL_AND_WORD[word], key=itemgetter(1), reverse=True)
    cm_data = sorted(CM[word], key=itemgetter(1), reverse=True)
    cm2_data = sorted(CM2[word], key=itemgetter(1), reverse=True)

    print(f'{word}:')
    print('PPMI: ', end='')
    i = 0
    best = []
    for w in ppmi_data:
        if i == 10:
            break
        if w[0] in best:
            continue
        best.append(w[0])
        print(f'{w[0]}, ', end='')
        i += 1
    print('')
    print('PSM: ', end='')
    i = 0
    best = []
    for w in psm_data:
        if i == 10:
            break
        if w[0] in best:
            continue
        best.append(w[0])
        print(f'{w[0]}, ', end='')
        i += 1
    print('')
    print('Grammatical and word collocations: ', end='')
    i = 0
    best = []
    for w in gaw_data:
        if i == 10:
            break
        if w[0] in best:
            continue
        best.append(w[0])
        print(f'{w[0]}, ', end='')
        i += 1
    print('')
    print('My own idea: ', end='')
    i = 0
    best = []
    for w in cm_data:
        if i == 10:
            break
        if w[0] in best:
            continue
        best.append(w[0])
        print(f'{w[0]}, ', end='')
        i += 1
    print('')
    print('My own idea with bonus points: ', end='')
    i = 0
    best = []
    for w in cm2_data:
        if i == 10:
            break
        if w[0] in best:
            continue
        best.append(w[0])
        print(f'{w[0]}, ', end='')
        i += 1
    print('')
    print('-' * 30)