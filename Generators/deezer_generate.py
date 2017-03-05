import fileinput
import json
import numpy as np
import sys

list_100 = []

path100 = "" # список песен, чтобы выводить названия, а не числа
path = "" # матрица попарной встречаемости

# считать топ 100
i = 0

with fileinput.input(files = path100) as f:
    for line in f:
        line_split = line.split("\t")
        title = line_split[0] + "\t" + line_split[1]
        list_100.append(title)
        i += 1

t_size = len(list_100)

mx = json.load(open(path))
mx_np = np.array(mx)
mx_norm = np.zeros((t_size, t_size))

for i in range(t_size):      # нормализация и она не оч, подумать над другими вариантами
    mx_row = mx_np[i]
    mx_norm[i] = 1.0*mx_row/np.sum(mx_row)

ans = "y"

while(ans == "y"):

    print("Songs:\n")

    for i in range(t_size):
        print(i, ":", list_100[i])

    n_t = int(input("Seed song number:\n"))
    pl_size = int(input("Playlist size:\n"))
    pl_l = [n_t]
    n_method = int(input("1 for max, 2 for random:\n"))

    if (n_method == 1):

        for i in range(pl_size - 1):
            line_t = mx[n_t]
            m_t = max(line_t)
            n_t = line_t.index(m_t)
            while (n_t in pl_l):
                line_t[n_t] = 0
                m_t = max(line_t)
                n_t = line_t.index(m_t)
            pl_l.append(n_t)

        print("\nPLAYLIST:")
        for i in range(pl_size):
            print(list_100[pl_l[i]])


    elif (n_method == 2):

        for i in range(pl_size - 1):
            line_t = mx[n_t]
            while (n_t in pl_l):
                line_t[n_t] = 0
                n_t = int(np.random.choice(range(t_size), 1, mx_norm.tolist()))
            pl_l.append(n_t)

        print("\nPLAYLIST:\n")
        for i in range(pl_size):
            print(list_100[pl_l[i]])

    ans = input("Continue? y/n\n")