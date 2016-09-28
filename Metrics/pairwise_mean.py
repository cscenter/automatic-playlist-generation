
# на входе массивы из тегов для каждой композиции  [[tags for track_1], [tags for track_2], ...]
# и функция, которая используется для метрики с двумя параметрами


def pairwise(array_tags, foo):

    s = 0
    l= len(array_tags)

    for i in range(l):
        for j in range((i+1),l):
            s += foo(array_tags[i], array_tags[j])


    n = l*(l-1)/2.0

    s = s/n

    return s


