from math import log, floor
import re
from operator import itemgetter
from sklearn.model_selection import KFold
import numpy as np

with open('./dane_pozytywizm/korpus_orzeszkowej.txt') as file:
    orzeszkowa_corpus = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())

with open('./dane_pozytywizm/korpus_prusa.txt') as file:
    prus_corpus = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())

with open('./dane_pozytywizm/korpus_sienkiewicza.txt') as file:
    sienkiewicz_corpus = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())


"""Below is defined Naive Bayes classification model."""


class NaiveBayesClassifier(object):
    def __init__(self, training_sets):
        """
        training_sets is a dict where:
        - key is a class,
        - value is a training set
        """
        self.classes = training_sets.keys()
        self.corpus_sizes = {}
        for c, corpus in training_sets.items():
            self.corpus_sizes[c] = len(corpus)
        self.p = self.train(training_sets)
        self.bigrams = self.make_bigrams(training_sets)

    def make_bigrams(self, corpuses):
        bigrams = {}

        for c, corpus in corpuses.items():
            for i in range(len(corpus)):
                if i + 1 < len(corpus):
                    if (corpus[i], corpus[i+1]) in bigrams:
                        if c in bigrams[(corpus[i], corpus[i+1])]:
                            bigrams[(corpus[i], corpus[i+1])][c] += 1
                        else:
                            bigrams[(corpus[i], corpus[i+1])][c] = 1
                    else:
                        bigrams[(corpus[i], corpus[i+1])] = {c: 1}

        return bigrams

    def train(self, corpuses):
        """
        p is a dict where:
        - key is a word,
        - value is a dict where:
            - key is a class
            - value is a probability of a word in that class
        """
        p = {}
        for c, corpus in corpuses.items():
            for word in corpus:
                if word in p:
                    if c in p[word]:
                        p[word][c] += 1
                    else:
                        p[word][c] = 1
                else:
                    p[word] = {c: 1}

        return p

    def test(self, test_set):
        probs = {}
        p_ci = 1 / len(self.classes)
        for c in self.classes:
            log_probs_sum = 0
            for i in range(len(test_set)):
                if i + 1 < len(test_set):
                    if (test_set[i], test_set[i + 1]) in self.bigrams and c in self.bigrams[(test_set[i], test_set[i + 1])]:
                        log_probs_sum += log(self.bigrams[(test_set[i], test_set[i + 1])][c] / self.p[test_set[i]][c])
                    else:
                        log_probs_sum += log((self.p[test_set[i]][c] + 1) / self.corpus_sizes[c]) if test_set[i] in self.p and c in self.p[test_set[i]] else log(1/self.corpus_sizes[c])
            probs[c] = p_ci + log_probs_sum

        ordered_probs = list(reversed(sorted(probs.items(), key=itemgetter(1))))
        return ordered_probs[0][0]


"""Below is k-fold Cross-Validation. (this may be wrong)"""

k = 10
kfold = KFold(k, shuffle=False)
accuracy = 0
i = 0

for train, test in kfold.split(orzeszkowa_corpus):
    data = {
        'Orzeszkowa': orzeszkowa_corpus[train],
        'Prus': prus_corpus,
        'Sienkiewicz': sienkiewicz_corpus,
    }
    naive_bayes = NaiveBayesClassifier(data)
    result = naive_bayes.test(orzeszkowa_corpus[test])
    print(i, result)
    if result == 'Orzeszkowa':
        accuracy += 1
    i += 1

for train, test in kfold.split(prus_corpus):
    data = {
        'Orzeszkowa': orzeszkowa_corpus,
        'Prus': prus_corpus[train],
        'Sienkiewicz': sienkiewicz_corpus,
    }
    naive_bayes = NaiveBayesClassifier(data)
    result = naive_bayes.test(prus_corpus[test])
    print(i, result)
    if result == 'Prus':
        accuracy += 1
    i += 1

for train, test in kfold.split(sienkiewicz_corpus):
    data = {
        'Orzeszkowa': orzeszkowa_corpus,
        'Prus': prus_corpus,
        'Sienkiewicz': sienkiewicz_corpus[train],
    }
    naive_bayes = NaiveBayesClassifier(data)
    result = naive_bayes.test(sienkiewicz_corpus[test])
    print(i, result)
    if result == 'Sienkiewicz':
        accuracy += 1
    i += 1

accuracy /= i
print(accuracy)


"""Testing on provided external data."""


accuracy = 0
i = 0

training_data = {
    'Orzeszkowa': orzeszkowa_corpus,
    'Prus': prus_corpus,
    'Sienkiewicz': sienkiewicz_corpus,
}

naive_bayes = NaiveBayesClassifier(training_data)

with open('./dane_pozytywizm/testy1/test_orzeszkowej.txt') as file:
    orzeszkowa_test = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())
    result = naive_bayes.test(orzeszkowa_test)
    print(f'expected: Orzeszkowa, result: {result}')
    if result == 'Orzeszkowa':
        accuracy += 1
    i += 1

for i in range(1, 23, 2):
    with open(f'./dane_pozytywizm/testy1/test_orzeszkowej{i}.txt') as file:
        orzeszkowa_test = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())
        result = naive_bayes.test(orzeszkowa_test)
        print(f'expected: Orzeszkowa, result: {result}')
        if result == 'Orzeszkowa':
            accuracy += 1
        i += 1

for i in range(0, 42, 2):
    with open(f'./dane_pozytywizm/testy1/test_prusa{i}.txt') as file:
        prus_test = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())
        result = naive_bayes.test(prus_test)
        print(f'expected: Prus, result: {result}')
        if result == 'Prus':
            accuracy += 1
        i += 1

for i in range(1, 55, 2):
    with open(f'./dane_pozytywizm/testy1/test_sienkiewicza{i}.txt') as file:
        sienkiewicz_test = np.array(re.sub('[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9 ]+', '', file.read().lower()).split())
        result = naive_bayes.test(sienkiewicz_test)
        print(f'expected: Sienkiewicz, result: {result}')
        if result == 'Sienkiewicz':
            accuracy += 1
        i += 1


print(f'Testing on {i} sets, accuracy: {accuracy/i}!')
