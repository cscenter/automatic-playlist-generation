import numpy as np


def weights_choice(weights, ind):  # ind -- номер предыдущей композиции

    w_ind = weights[ind]
    weights_2 = [abs(w - w_ind) for w in weights]

    l_w = len(weights)
    indices = [i for i in range(l_w)]

    del weights_2[ind]
    del indices[ind]
   
    mult = 1.0/sum(weights)
    weights_norm = [w*mult for w in weights_2]
    
    ind_new = np.random.choice(indices, 1, weights_norm)

    return ind_new



def pairwise_choice(dist):   # вектор попарных расстояний для предыдущей композиции

    indices = [i for i in range(len(dist))]

    mult = 1.0/sum(dist)
    dist_norm = [d*mult for d in dist]

    ind_new = np.random.choice(indices, 1, dist_norm)

    return ind_new
