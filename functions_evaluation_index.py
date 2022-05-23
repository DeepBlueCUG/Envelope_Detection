import numpy as np


def sitar(data):

    length_data = len(data)
    sitar_list = []
    for i in range(1, length_data - 1):
        current_sitar = (data[i - 1] + data[i + 1]) / 2 - data[i]
        sitar_list.append(abs(current_sitar))

    return np.mean(np.array(sitar_list))


def ac(data_x, data_y):

    x = np.array(data_x)
    y = np.array(data_y)

    mean_x = np.mean(x)
    mean_y = np.mean(y)
    member = np.dot(x - y, x - y)
    denominator = np.dot(np.abs(mean_x - mean_y) + np.abs(x - mean_x), np.abs(mean_x - mean_y) + np.abs(y - mean_y))
    # denominator = np.dot(np.abs(x - mean_x), np.abs(y - mean_y))

    return 1 - member / denominator


def rmse(data_x, data_y):

    x = np.array(data_x)
    y = np.array(data_y)

    return np.sqrt(np.mean(np.dot(x - y, x - y)))