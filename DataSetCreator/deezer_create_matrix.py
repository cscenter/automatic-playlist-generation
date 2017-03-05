import fileinput
import json

path = "" # плейлисты для тестового множества -- вывод из deezer_create_test.py
out1 = "" # матрица попарной встречаемости -- сколько раз в одном плейлисте

t_size = 100

m = [[0] * t_size for _ in range(t_size)]

for j in range(t_size):
    with fileinput.input(files = path) as f:
        tmp_pl = []
        for line in f:
            tmp_pl = json.loads(line)

            if j in tmp_pl:
                for k in range(len(tmp_pl)):
                    m[j][tmp_pl[k]] += 1
        m[j][j] = 0


with open(out1, 'w') as f_out:
    json.dump(m, f_out)