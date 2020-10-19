corpus_limited_to_tokenize = []
corpus_limited_to_correct = []
corpus_words = set()


with open('./polish_corpora_limited.txt', encoding='utf-8') as file:
    for i, line in enumerate(file):
        line_edited = line.lower().strip()
        corpus_words.update(line_edited.split())
        corpus_limited_to_tokenize.append(line_edited.replace(' ', ''))
        corpus_limited_to_correct.append(line)


def max_match(sentence):
    tokens = []
    i = 0
    while i < len(sentence):
        max_word = ''
        for j in range(i, len(sentence)):
            temp_word = sentence[i:j + 1]
            if temp_word in corpus_words and len(temp_word) > len(max_word):
                max_word = temp_word
        if max_word == '':
            return tokens
        i = i + len(max_word)
        tokens.append(max_word)
    return tokens


def max_match_reverse(sentence):
    tokens = []
    i = len(sentence) - 1
    while i >= 0:
        max_word = ''
        for j in range(i, -1, -1):
            temp_word = sentence[j - 1:i]
            if temp_word in corpus_words and len(temp_word) > len(max_word):
                max_word = temp_word
        if max_word == '':
            return tokens
        i = i - len(max_word)
        tokens.append(max_word)
    return tokens


# Text similarity metrics:
def words_intersection(tokens, sentence):
    tokens_set = set(tokens)
    sentence_set = set(sentence.lower().strip().split())
    intersection = tokens_set.intersection(sentence_set)
    return len(intersection) / (len(tokens_set) + len(sentence_set) - len(intersection))


max_match_words_intersection_error = 0
max_match_reverse_words_intersection_error = 0

for i, item in enumerate(corpus_limited_to_tokenize):
    tokens_max = max_match(item)
    tokens_max_reverse = max_match_reverse(item)
    max_match_words_intersection_error += words_intersection(tokens_max, corpus_limited_to_correct[i])
    max_match_reverse_words_intersection_error += words_intersection(tokens_max_reverse, corpus_limited_to_correct[i])

max_match_words_intersection_error /= len(corpus_limited_to_tokenize)
max_match_reverse_words_intersection_error /= len(corpus_limited_to_tokenize)

print(f'MaxMatch words intersection error: {max_match_words_intersection_error}')
print(f'MaxMatch reverse words intersection error: {max_match_reverse_words_intersection_error}')
