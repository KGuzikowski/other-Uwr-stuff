from typing import Optional
import re
from operator import itemgetter

tags = {}
PAN_TADEUSZ_SAMPLE_TAGS = []

with open('./supertags.txt', encoding='utf-8') as file:
    for line in file:
        word, tag = line.split()
        tags[word] = tag


def assume_tag(word: str) -> Optional[str]:
    suffix = word[-3:]
    suffix2 = word[-2:]
    possible_tags = {}
    for x, tag in tags.items():
        if x[-3:] == suffix:
            if tag in possible_tags:
                possible_tags[tag] += 1
            else:
                possible_tags[tag] = 1
        if x[-2:] == suffix2:
            if tag in possible_tags:
                possible_tags[tag] += 1
            else:
                possible_tags[tag] = 1
    if len(possible_tags.keys()) == 0:
        return None
    else:
        a = sorted(possible_tags.items(), key=itemgetter(1), reverse=True)
        return a[0][0]


with open('./pan_tadeusz_tags.txt', "w") as final_data:
    with open('./pan_tadeusz.txt', encoding='utf-8') as file:
        for line in file:
            data = re.sub('[^a-ząćęłńóśźż ]+', '', line.strip().lower()).split()
            if len(data) > 0:
                sen_tags = []
                for word in data:
                    if word in tags:
                        sen_tags.append(tags[word])
                    else:
                        tag = assume_tag(word)
                        if tag:
                            sen_tags.append(tag)
                final_data.write(" ".join(sen_tags) + '\n')

