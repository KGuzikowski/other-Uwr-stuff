import random

words_map_2 = {}
words_map_3 = {}

'''Reading from file for task 2'''
with open('../poleval_2grams.txt', encoding='utf-8') as file:
    for line in file:
        words = line.split()
        if int(words[0]) < 3:
            continue
        if words[1] in words_map_2:
            words_map_2[words[1]].append(words[2])
        else:
            words_map_2[words[1]] = [words[2]]

with open('../poleval_3grams.txt', encoding='utf-8') as file:
    for line in file:
        words = line.split()
        if int(words[0]) < 3:
            continue
        if words[1] in words_map_3:
            words_map_3[words[1]].add(words[2])
        else:
            words_map_3[words[1]] = {words[2]}
        if len(words) == 4:
            if words[2] in words_map_3:
                words_map_3[words[2]].add(words[3])
            else:
                words_map_3[words[2]] = {words[3]}

'''Reading from file for task 3'''
with open('../poleval_2grams.txt', encoding='utf-8') as file:
    for line in file:
        words = line.split()
        if int(words[0]) < 3:
            continue
        if words[1] in words_map_2:
            words_map_2[words[1]].append((words[2], int(words[0])))
        else:
            words_map_2[words[1]] = [(words[2], int(words[0]))]

with open('../poleval_3grams.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        words = line.split()
        if i > 500000:
            break
        if words[1] in words_map_3:
            if words[2] not in words_map_3[words[1]]:
                words_map_3[words[1]].append((words[2], int(words[0])))
            else:
                for item in words_map_3[words[1]]:
                    if item[0] == words[2]:
                        item[1] += int(words[0])
                        break
        else:
            words_map_3[words[1]] = [(words[2], int(words[0]))]

        if len(words) == 4:
            if words[2] in words_map_3:
                if words[3] not in words_map_3[words[2]]:
                    words_map_3[words[2]].append((words[3], int(words[0])))
                else:
                    for item in words_map_3[words[2]]:
                        if item[0] == words[3]:
                            item[1] += int(words[0])
                            break
            else:
                words_map_3[words[2]] = [(words[3], int(words[0]))]


# choice arg is a random.choice using regular list for tas 2
# and a choice function (defined below)
def generate_sentences(word, words_map, choice):
    print(word.title(), end=' ')
    while True:
        if word in words_map and len(words_map[word]) > 0:
            word = choice(list(words_map[word]))
            print(word, end=' ')
        else:
            print('')
            return


# options is a list of tuples
def choice(options):
    choose_from = []
    for item in options:
        for _ in range(item[1]):
            choose_from.append(item[0])
    return random.choice(choose_from)


# task 2
# generate_sentences(random.choice(list(words_map_2.keys())), words_map_2, random.choice)
# generate_sentences(random.choice(list(words_map_3.keys())), words_map_3, random.choice)

# task 3
# generate_sentences(random.choice(list(words_map_2.keys())), words_map_2, choice)
# generate_sentences(random.choice(list(words_map_3.keys())), words_map_3, choice)
