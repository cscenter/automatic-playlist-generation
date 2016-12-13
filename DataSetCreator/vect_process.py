import json

# на вход два файла -- массив векторов тегов last.fm и
# массив векторов audio_features
# из каждого новый файл, где нет нулевых векторов
# отдельно индексы, соотв. оригиналу
# плюс скомбинировать их, объединяя ненулевые
# для обоих массивов векторы



def non_zeros(file_in, file_out, idx_out):

    data = json.load(open(file_in))
    ids = open(idx_out, "w")

    new_list = []

    l_d = len(data)

    for i in range(l_d):
        vect = data[i]
        if (sum(vect) > 0):
            new_list.append(vect)
            ids.write(str(i))
            ids.write("\n")

    print(l_d, len(new_list))

    with open(file_out, "w") as f_out:
        json.dump(new_list, f_out)

    return



# file_in1 -- векторы по тегам last.fm
# file_in2 -- векторы audio_features

def combine(file_in1, file_in2, file_out, idx_out):

    data1 = json.load(open(file_in1))
    data2 = json.load(open(file_in2))
    ids = open(idx_out, "w")

    new_list = []

    if (len(data1) != len(data2)):
        print("check files")
        l_d = len(data1)

    else:

        for i in range(l_d):
            vect1 = data1[i]
            vect2 = data2[i]
            if ((sum(vect1) > 0) and (sum(vect2) > 0)):
                vect1.extend(vect2)
                print(vect1)
                new_list.append(vect1)
                ids.write(str(i))
                ids.write("\n")

    print(l_d, len(new_list))

    with open(file_out, "w") as f_out:
        json.dump(new_list, f_out)


    return

