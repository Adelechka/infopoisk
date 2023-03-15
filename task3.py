def inverted_index():
    inverted_index = {}

    for i in range(100):
        text_file = open("output_task2/lemmas" + str(i) + '.txt', 'r', encoding='cp1251')
        lines = text_file.readlines()
        for line in lines:
            lemma = line.split(":")[0]
            if lemma in inverted_index:
                updated_inverted_index = inverted_index[lemma]
                updated_inverted_index.append(i)
                inverted_index[lemma] = updated_inverted_index
            else:
                inverted_index[lemma] = [i]

    return inverted_index


def write(inverted_index):
    with open("output_task3/inverted_lemmas.txt", "w", encoding='cp1251') as f:
        for key, value in inverted_index.items():
            f.write('%s:%s\n' % (key, value))


if __name__ == '__main__':
    inverted_index = inverted_index()
    write(inverted_index)
