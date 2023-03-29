import math
import re
from math import log
from os import listdir
from os.path import isfile, join

import nltk
import pymorphy2
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


if __name__ == '__main__':
    stopwords = stopwords.words("russian")
    output_task1 = "output/"
    output_task2 = "output_task2/"
    output_task4 = "output_task4/"
    filenames = listdir(output_task1)
    count = 100

    lemmatizer = pymorphy2.MorphAnalyzer(lang='ru')


    for i in range(100):
        if i is not 14:
            try:
                text_file = open(output_task1 + str(i) + '.txt', 'r', encoding='cp1251')
                text = BeautifulSoup(text_file, 'html.parser').get_text().lower()
                tokens = nltk.word_tokenize(text)
                for token in tokens:
                    if token in stopwords or not token.isalpha() or not re.match(r"[а-яё]", token) or len(token) <= 2:
                        tokens.remove(token)
            except:
                continue

            #tf for tokens
            tokens_set = set(tokens)
            tokens_tf_dict = dict.fromkeys(tokens_set, 0.0)
            tokens_count = len(tokens)
            for token in tokens:
                tokens_tf_dict[token] += 1
            for k, v in tokens_tf_dict.items():
                tokens_tf_dict[k] = float(v) / float(tokens_count)

            #idf for tokens
            tokens_idf_dict = dict.fromkeys(tokens_set, 0.0)
            N = 100

            for j in range(100):

                try:
                    tokens_in_file = [token.split(':') for token in open(output_task2 + 'tokens' + str(j) + '.txt').read().splitlines()]
                    tokens_in_file = [element[0] for element in tokens_in_file]
                    for word in tokens_in_file:
                        if word in tokens_set:
                            tokens_idf_dict[word] += 1.0
                except:
                    continue

            for k, v in tokens_tf_dict.items():
                tokens_idf_dict[k] = math.log(N / float(v))

            print(tokens_tf_dict)
            print(tokens_idf_dict)

            lemmas = list()
            for token in tokens:
                lemmas.append(lemmatizer.parse(token)[0].normal_form)

            lemmas_set = set(lemmas)
            lemmas_tf_dict = dict.fromkeys(lemmas_set, 0.0)
            lemmas_count = len(lemmas)
            for lemma in lemmas:
                lemmas_tf_dict[lemma] += 1
            for k, v in lemmas_tf_dict.items():
                lemmas_tf_dict[k] = float(v) / float(lemmas_count)


            lemmas_idf_dict = dict.fromkeys(lemmas_set, 0.0)
            N = 100

            for j in range(100):
                try:
                    lemmas_in_file = [lemma.split(':') for lemma in
                                      open(output_task2 + 'lemmas' + str(j) + '.txt').read().splitlines()]
                    lemmas_in_file = [element[0] for element in lemmas_in_file]
                    for word in lemmas_in_file:
                        if word in lemmas_set:
                            lemmas_idf_dict[word] += 1.0
                except:
                    continue

            for k, v in lemmas_tf_dict.items():
                lemmas_idf_dict[k] = math.log(N / float(v))

            print(lemmas_tf_dict)
            print(lemmas_idf_dict)

            tokens_file = open(output_task4 + 'tokens_tf_idf' + str(i) + '.txt', 'w')
            for k, v in tokens_tf_dict.items():
                tokens_file.write(str(k) + " " + str(tokens_tf_dict[k]) + " " + str(tokens_idf_dict[k]) + "\n")

            lemmas_file = open(output_task4 + 'lemmas_tf_idf' + str(i) + '.txt', 'w')
            for k, v in lemmas_tf_dict.items():
                lemmas_file.write(str(k) + " " + str(lemmas_idf_dict[k]) + " " + str(math.log(100 / float(lemmas_idf_dict[k]))) + "\n")
