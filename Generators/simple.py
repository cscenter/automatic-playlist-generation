import numpy as np


def weights_choice(weights, ind):  # ind -- номер предыдущей композиции

    l_w = len(weights)

    w_ind = weights[ind]

    weights_np = np.array(weights)
    w_ind_np = np.repeat(w_ind, l_w)
    
    weight_diff = np.absolute(weights_np - w_ind_np)
 
    indices = np.arange(l_w)

    weights_del = np.delete(weight_diff, ind)
    indices_del = np.delete(indices, ind)

    mult = 1.0/np.sum(weights_del)
    weights_norm = mult*weights_del
    
    ind_new = np.random.choice(indices_del.tolist(), 1, weights_norm.tolist())

    return ind_new



def pairwise_choice(dist):   # вектор попарных расстояний для предыдущей композиции

    l_d = len(dist)

    dist_np = np.array(dist)
    indices = np.arange(l_d)

    mult = 1.0/np.sum(dist_np)
    dist_norm = mult*dist_np

    ind_new = np.random.choice(indices.tolist(), 1, dist_norm.tolist())

    return ind_new



