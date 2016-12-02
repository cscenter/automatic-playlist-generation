import json

file_in = "50K_corr.txt"   # вида p_id<tab>artist<tab>title
file_out = "50K_better.txt"


# если в плейлисте хотя бы 5 песен, отправлять его в новый файл,
# при этом убрав из названий (, [ и /, в тегах их не бывает обычно


def better_title(title):

    if (title.find("(") != -1):
        title = title.split("(")[0]

    if (title.find("[") != -1):
        title = title.split("[")[0]

    if (title.find("/") != -1):
        title = title.split("/")[0]


    return title




f = open(file_in, 'r')
f_out = open(file_out, 'w')

p_id_old = ""
cnt = 0
lines = []


for line in f:
    tab_sep = line.split('\t')
    p_id = tab_sep[0]
    #artist = tab_sep[1]
    #title = tab_sep[2].split('\n')[0]

    if (p_id == p_id_old):      # просто копить
        cnt += 1
        lines.append(line)

    else:                       # менять старый, считать сколько накопилось, править строчки и записывать

        if (cnt > 4):
            for track in lines:
                    t_sep = track.split('\t')
                    t_p_id = t_sep[0]
                    artist = t_sep[1]
                    artist = artist.replace("/", "")
                    title = t_sep[2].split('\n')[0]
                    title = better_title(title)
                    new_line = p_id + "\t" + artist + "\t" + title

                    f_out.write(new_line)
                    f_out.write("\n")

        cnt = 0
        p_id_old = p_id
        lines = []