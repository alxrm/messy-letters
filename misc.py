def last_index_match(collection, predicate):
    last = -1

    for i in range(0, len(collection)):
        if predicate(collection[i]):
            last = i

    return last


