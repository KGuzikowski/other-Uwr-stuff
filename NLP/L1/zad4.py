from itertools import permutations
from queue import PriorityQueue

bigram = {}
trigram = {}

with open('../poleval_2grams.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i < 2000:
            words = line.split()
            bigram[(words[1], words[2])] = int(words[0])
        else:
            break

with open('../poleval_3grams.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i < 2000:
            words = line.split()
            trigram[(words[1], words[2], words[3])] = int(words[0])
        else:
            break

examples = [
    'Nastąpiło przedawnienie pewnych ustalonych skali i obszarów lasów.',
    'Premiowanie beneficjentów fundacji przebiegło pomyślnie.',
]

for item in examples:
    available_words = item[:-1].lower().split()
    words_permutations = permutations(available_words)
    queue = PriorityQueue()

    for option in words_permutations:
        score = 0
        for i in range(len(option) - 1):
            if (option[i], option[i+1]) in bigram:
                score += bigram[(option[i], option[i+1])]
            if i < len(option) - 2 and (option[i], option[i+1], option[i+2]) in trigram:
                score += trigram[(option[i], option[i+1], option[i+2])] * 10
        queue.put((-score, ' '.join(option)))

    for i in range(10):
        sentence = queue.get()
        print(f'{-sentence[0]}: {sentence[1]}')
    print('-'*20)
