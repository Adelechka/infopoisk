import math
import os
import re

import nltk
import pymorphy2
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

if __name__ == '__main__':
    output_task1 = 'output/'
    output_task2 = 'output_task2/'
    output_task4 = 'output_task4/'
    lemmas_path = 'output_task2/lemmas.txt'
    index_path = 'index.txt'
    stopwords = stopwords.words("russian")
    lemmatizer = pymorphy2.MorphAnalyzer(lang='ru')

    with open(lemmas_path, "r", encoding="cp1251") as f:
        lemmas = [line.split(':')[0] for line in f.readlines()]

    with open(index_path, "r", encoding="cp1251") as f:
        index = {filename: link for filename, link in (link.split(' - ') for link in f.readlines())}

    tokens_all = []
    for i in range(100):
        try:
            text_file = open(output_task1 + str(i) + '.txt', 'r', encoding='cp1251')
            text = BeautifulSoup(text_file, 'html.parser').get_text().lower()
            tokens = nltk.word_tokenize(text)
            token = 0
            while token < len(tokens):
                if tokens[token] in stopwords or not tokens[token].isalpha() \
                        or not re.match(r"[а-яё]", tokens[token]) or len(tokens[token]) <= 2:
                    tokens.remove(tokens[token])
                token += 1
            tokens_all += tokens
        except:
            continue

    lemmas_all = []
    for token in tokens_all:
        lemmas_all.append(lemmatizer.parse(token)[0].normal_form)
    lemmas_idf_dict = dict.fromkeys(lemmas, 0.0)
    N = 100

    for j in range(100):
        try:
            lemmas_in_file = [lemma.split(':') for lemma in
                              open(output_task2 + 'lemmas' + str(j) + '.txt').read().splitlines()]
            lemmas_in_file = [element[0] for element in lemmas_in_file]
            for word in lemmas_in_file:
                if word in lemmas:
                    lemmas_idf_dict[word] += 1.0
        except:
            continue

    for k, v in lemmas_idf_dict.items():
        lemmas_idf_dict[k] = math.log(N / float(v))

    print(len(lemmas_idf_dict))

    # tf_idfs = {}
    # for file in os.listdir(output_task4):
    #     if file.startswith("lemmas"):
    #         with open(os.path.join(output_task4, file), 'r', encoding='cp1251') as f:
    #             key = file.lstrip("lemmas")
    #             tf_idfs[key] = defaultdict(float)
    #             for line in f.readlines():
    #                 token = line.split(": ")[0]
    #                 tf, idf = line.split(": ")[1].split()
    #                 if token in lemmas:
    #                     tf_idfs[key][lemmas.index(token)] = float(tf) * float(idf)
    # print(tf_idfs)
