import os

N = 100
K = 10
unigrams = {}

with open('./unigram.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        data = line.split()
        if int(data[0]) < N:
            break
        unigrams[data[1]] = data[0]

with open('./data_for_task_5_unsorted.txt', "w") as final_data:
    with open('../poleval_2grams.txt', encoding='utf-8') as bigram:
        for line in bigram:
            uni_keys = unigrams.keys()
            data = line.split()
            if data[1] in uni_keys and int(data[0]) >= K:
                final_data.write(f'{unigrams[data[1]]} {data[1]}\n')
                del unigrams[data[1]]
            elif data[2] in uni_keys and int(data[0]) >= K:
                final_data.write(f'{unigrams[data[2]]} {data[2]}\n')
                del unigrams[data[2]]

command1 = 'sort -nr data_for_task_5_unsorted.txt > data_for_task_5.txt'
command2 = 'rm data_for_task_5_unsorted.txt'
os.system(command1)
os.system(command2)
