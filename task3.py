
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
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


def boolean_search(query, inverted_index_dict):
    query = query.lower().split()
    results = set()
    for term in query:
        if term == 'and':
            continue
        elif term == 'or':
            continue
        elif term == 'not':
            continue
        else:
            if term in inverted_index_dict:
                results.update(inverted_index_dict[term])
                print(len(results))
    for i, term in enumerate(query):
        if term == 'and':
            if query[i-1] in inverted_index_dict and query[i+1] in inverted_index_dict:
                results.intersection_update(intersection(inverted_index_dict[query[i-1]], inverted_index_dict[query[i+1]]))
        elif term == 'or':
            if query[i-1] in inverted_index_dict and query[i+1] in inverted_index_dict:
                results.__ior__(inverted_index_dict[query[i-1]] + inverted_index_dict[query[i+1]])
        elif term == 'not':
            if query[i+1] in inverted_index_dict:
                results = results - set(inverted_index_dict[query[i+1]])
    return sorted(results)


if __name__ == '__main__':
    inverted_index_dict = inverted_index()
    write(inverted_index_dict)
    # вектор or бок or раритет
    query = input()
    print(boolean_search(query, inverted_index_dict))
    #
    # result = set([1, 2, 3])
    # result.__ior__(set([4]))
    # print(result)