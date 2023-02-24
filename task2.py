import re
from os import listdir
from os.path import isfile, join

import codecs
import nltk as nltk
import pymorphy2 as pymorphy2
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


if __name__ == '__main__':
    output_task1 = "output/"
    output_task2 = "output_task2/"

    files = [output_task1 + f for f in listdir(output_task1) if isfile(join(output_task1, f))]

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    stopwords = stopwords.words("russian")
    lemmatizer = pymorphy2.MorphAnalyzer(lang='ru')

    tokens = list()
    lemmas = {}

    for file in files:
        html = codecs.open(file, 'r', encoding='cp1251')
        try:
            data = html.read()
            text = BeautifulSoup(data, 'html.parser').get_text().lower()
            tokens += nltk.word_tokenize(text)
        except:
            continue

        cleaning1 = set()
        for word in tokens:
            try:
                if word.isalpha() and not re.match(r"[a-z]", word):
                    cleaning1.add(word)
            except:
                continue

        cleaning2 = set()
        for word in cleaning1:
            try:
                if not word in stopwords:
                    cleaning2.add(word)
            except:
                continue

    tokens_file = open(output_task2 + 'tokens.txt', 'w')
    for token in list(cleaning2):
        tokens_file.write(token + "\n")
    tokens_file.close()

    for token in cleaning2:
        lemma = lemmatizer.parse(token)[0].normal_form
        if lemmas.keys().__contains__(lemma):
            lemmas[lemma] += [token]
        else:
            lemmas[lemma] = [token]

    lemmas_file = open(output_task2 + 'lemmas.txt', 'w')
    for lemma in lemmas:
        tokens = ' '
        for token in lemmas[lemma]:
            tokens += ' ' + token
        lemmas_file.write(lemma + ":" + tokens + '\n')
    lemmas_file.close()
