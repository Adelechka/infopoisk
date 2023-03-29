import nltk
import numpy as np
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import pandas as pd
from pymystem3 import Mystem
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stopwords_ru = stopwords.words("russian")
stopwords_en = stopwords.words("english")
stopwords_all = stopwords_en + stopwords_ru

tokens = open('output_task2/tokens.txt', encoding='cp1251').read().splitlines()
lemmas = [word.split(' ')[0] for word in open('output_task2/lemmas.txt', encoding='cp1251').read().splitlines()]

lemmatizer_en = WordNetLemmatizer()
lemmatizer_ru = Mystem()


def coef_otaiai(df1, df2):
    merged_df = pd.merge(df1, df2, on='word')
    x = np.array(merged_df['td-idf_x'])
    y = np.array(merged_df['td-idf_y'])
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_dev = x - x_mean
    y_dev = y - y_mean
    numerator = np.sum(x_dev * y_dev)
    denominator = np.sqrt(np.sum(x_dev ** 2) * np.sum(y_dev ** 2))
    print(f" x {x}")
    print(f" y {y}")
    print(f" x_meam {x_mean}")
    print(f" y_mean {y_mean}")
    print(f" x_dev {x_dev}")
    print(f" y_dev {y_dev}")
    return numerator / denominator


def get_tokens(text: str):
    text_tokens = nltk.word_tokenize(text)
    almost_clean_tokens = set([w for w in text_tokens if not re.search(r"[^a-zA-Zа-яА-ЯёЁ]", w)])
    clean_tokens = [w for w in almost_clean_tokens if w not in stopwords_all and len(w) > 1]
    return clean_tokens


def get_lemmas(text: str):
    text_tokens = get_tokens(text)
    text_lemmas = []
    for token in text_tokens:
        if re.search(r"[a-zA-Z]", token):
            lemma = lemmatizer_en.lemmatize(token)
        else:
            lemma = lemmatizer_ru.lemmatize(token)[0]
        text_lemmas.append(lemma)
    return text_lemmas


def process(input_str):
    texts = [input_str]
    tokens_vectorizer = TfidfVectorizer(analyzer=get_tokens, vocabulary=tokens)

    tokens_matrix = tokens_vectorizer.fit_transform(texts)

    tokens_idf = pd.DataFrame(tokens_vectorizer.idf_, index=tokens, columns=["idf"])

    tokens_tfidf = pd.DataFrame(tokens_matrix.T.todense(), index=tokens, columns=["tf-idf"])

    tokens_result_df = pd.concat([tokens_idf, tokens_tfidf], axis=1)
    tokens_result_df = tokens_result_df.rename(columns={tokens_result_df.columns[0]: 'word'})

    tokens_file = open(f"tokens.txt", "w", encoding='cp1251')
    tokens_file.write(tokens_result_df.to_csv(sep=" ", header=False))
    tokens_file.close()

    tokens_for_query_read = pd.read_csv(
        'tokens.txt',
        delimiter=' ',
        names=['word', 'idf', 'td-idf'],
        encoding='cp1251'
    )

    dict_ans = {}

    output_directory = "output_task4/"

    for i in range(100):
        tokens_for_text_read = pd.read_csv(
            f'{output_directory}lemmas_tf_idf{i}.txt',
            delimiter=' ',
            names=['word', 'idf', 'td-idf'],
            encoding='cp1251'
        )
        if i == 1:
            print(tokens_for_text_read)
        dict_ans[i] = coef_otaiai(tokens_for_text_read, tokens_for_query_read)

    sorted_dict_ans = dict(sorted(dict_ans.items(), key=lambda x: x[1]))
    sorted_keys = sorted(sorted_dict_ans, key=sorted_dict_ans.get, reverse=True)

    return sorted_keys


def manual_mode():
    print("Салам брат, я поисковик, дон, введите ваш запрос!")
    input_str = input()

    # texts = ["Плотность населения была высокой в Южной Европе"]
    query = [input_str]

    for key in process(query):
        print("text " + str(key))


# manual_mode()