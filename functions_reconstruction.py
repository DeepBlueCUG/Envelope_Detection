# The reconstruction methods
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy import interpolate



def envelope_detection(data_original: list, t: list, rtc):

    data_envelope_detection = [data_original[0]]
    t_envelope_detection = [t[0]]

    index_list = list(range(len(data_original)))
    index_envelope_detection = [0]

    length_data = len(data_original)
    for i in range(1, length_data):
        check = data_original[i]
        if check > data_envelope_detection[-1]:
            data_envelope_detection.append(check)
            t_envelope_detection.append(t[i])
            index_envelope_detection.append(index_list[i])
        else:

            t_distance = t[i] - t_envelope_detection[-1]
            temp = math.pow(rtc / (rtc + 1), int(t_distance))
            compute = data_envelope_detection[-1] * temp
            if compute < check:
                data_envelope_detection.append(check)
                t_envelope_detection.append(t[i])
                index_envelope_detection.append(index_list[i])
            else:
                data_envelope_detection.append(compute)

    data_redetected = []
    for index in index_envelope_detection:
        data_redetected.append(data_original[index])

    if t_envelope_detection[-1] != t[-1]:
        t_envelope_detection.append(t[-1])
        data_redetected.append(data_original[-1])
    linear_interploate = interpolate.interp1d(t_envelope_detection, data_redetected, kind="slinear")
    linear_interpolated = linear_interploate(t)
    linear_interpolated = list(linear_interpolated)

    # length_envelope = len(data_redetected)
    # linear_interpolated.append(length_envelope/len(data_original))

    return linear_interpolated



# Harmonic Analysis of Timeseries
class hants:
    def __init__(self, n: int):
        self.order = n

    def trigonometric_function(self, t):
        result = []
        for i in range(len(t)):
            element = [t[0]]
            for j in range(self.order):
                time_radians = t[i] * 2 * (j + 1) * math.pi
                element.append(math.sin(time_radians))
                element.append(math.cos(time_radians))
            result.append(element)

        return np.array(result)

    def hants(self, data_original: list, t: list, t_fit: list):

        t_array = np.array(t)
        t_original = t_array / t[-1]
        data = np.array(data_original)

        # t_list = range(1, len(data_original) + 1)
        # t_array = np.array(t_list)
        # t = t_array / len(data_original)
        # data = np.array(data_original)

        #x = self.waves_overlay(t)
        x = self.trigonometric_function(t_original)

        model = LinearRegression(fit_intercept=True)
        # model.fit(x.transpose(), data.transpose())
        # score = model.score(x.transpose(), data.transpose())
        model.fit(x, data)
        # score = model.score(x, data)
        # print(score)
        x_new = np.array(t_fit)
        x_new = x_new / x_new[-1]
        t_new = self.trigonometric_function(x_new)

        y_fit = model.predict(t_new)

        # coefficient = model.coef_
        # constant = model.intercept_
        # harmonic_1 = x[0, :] * coefficient[0] + x[1, :] * coefficient[1]
        # harmonic_2 = x[2, :] * coefficient[2] + x[3, :] * coefficient[3]
        # harmonic_3 = x[4, :] * coefficient[4] + x[5, :] * coefficient[5]
        # harmonic = np.row_stack((harmonic_1, harmonic_2, harmonic_3))

    # x = np.array(x)
    # y = np.array(y)
    # model = LinearRegression(fit_intercept=True)
    # model.fit(x[:, np.newaxis], y)
    #
    # x_fit = np.linspace(0, 1, 1000)
    # y_fit = model.predict(x_fit[:, np.newaxis])

    # data_output = {'x': x, 'y': y, 'x_fit': x_fit, 'y_fit': y_fit}

        return y_fit.transpose()


def asymmetric_gaussians(data_original: list):

    for i in range(len(data_original)):
        if data_original[i] <= 0:
            data_original[i] = 0.001
    t_list = range(1, len(data_original) + 1)
    t = np.array(t_list)
    data = np.array(data_original)

    #max_data = np.max(data)
    max_index = np.unravel_index(np.argmax(data), np.shape(data))
    #y_logarithm = np.log(data)
    y_logarithm = data


    # figure = plt.figure()
    # axe = figure.add_subplot(1, 1, 1)
    # axe.plot(y_logarithm, ls="-", lw=2, label="y_logarithm")
    # plt.show()


    t_left = t[: max_index[0]]
    y_left = y_logarithm[0: max_index[0]]
    t_right = t[max_index[0]:]
    y_right = y_logarithm[max_index[0]:]

    def function(x, a, b, c, d):
        return a + b * np.exp(-1 * (x / c) ** d)

    parameter_left = (max_index - t_left)
    # print(parameter_left)
    # print(y_left)
    popt_left, pcov = curve_fit(function, parameter_left, y_left, bounds=([0, 0, 30, 2], [1, 1, 100, 10]))
    fitted_left = []
    for item in parameter_left:
        fitted = popt_left[0] + popt_left[1] * np.exp(-1 * (item / popt_left[2]) ** popt_left[3])
        fitted_left.append(fitted)

    parameter_right = (t_right - max_index)
    popt_right, pcov = curve_fit(function, parameter_right, y_right, bounds=([0, 0, 30, 2], [1, 1, 100, 10]))
    fitted_right = []
    for item in parameter_right:
        fitted = popt_right[0] + popt_right[1] * np.exp(-1 * (item / popt_right[2]) ** popt_right[3])
        fitted_right.append(fitted)

    fitted_data = fitted_left + fitted_right
    fitted_data = np.array(fitted_data)

    # return fitted_data

    parameter = [popt_left]
    parameter.append(popt_right)

    return parameter

# The Best Index Slope Extraction
def bise(data_original: list, window_size, increase_threshold, decrease_threshold):

    bise_extracted = [data_original[0]]
    x_bise = [0]
    data = np.array(data_original)
    for i in range(1, len(data_original) - window_size - 1):

        if x_bise[-1] >= i:
            continue
        else:
            if data[i] >= data[i - 1]:
                difference = data[i] - data[i - 1]
                if difference < increase_threshold:
                    bise_extracted.append(data[i])
                    x_bise.append(i)
            else:
                sliding_window = data[i + 1: i + window_size]
                find = False
                for j in range(len(sliding_window)):
                    if sliding_window[j] >= data[i] * (1 + decrease_threshold):
                        bise_extracted.append(data[i + 1 + j])
                        x_bise.append(i + 1 + j)
                        find = True
                        break
                if find == False:
                    bise_extracted.append(data[i])
                    x_bise.append(i)

    # if x_bise[-1] != len(data_original) - 1 - window_size:
    #     x_bise.append(len(data_original) - 1 - window_size)
    #     bise_extracted.append(data_original[len(data_original) - 1 - window_size])
    if x_bise[-1] != len(data_original) - 1:
        x_bise.append(len(data_original) - 1)
        bise_extracted.append(data_original[-1])
    linear_interploate = interpolate.interp1d(x_bise, bise_extracted, kind="slinear")
    x_new = []
    x_new = range(len(data_original))
    linear_interpolated = linear_interploate(x_new)
#    linear_interpolated = np.array(linear_interpolated)

    return linear_interpolated


# Savitzky-Golay Filter
def sg_filtering(data: list, half_window: int, order: int):
    # half_size = (window_size - 1) / 2
    # odata = data[:]
    #
    # for i in range(half_size):
    #     odata.insert(0, odata[0])
    #     odata.insert(len(odata), odata[len(odata) - 1])

    window_size = half_window * 2 + 1
    coefficient = []
    for i in range(window_size):
        distance = i - window_size
        row = [distance**j for j in range(order)]
        coefficient.append(row)
    coefficient = np.mat(coefficient)

    coefficient_b = (coefficient * (coefficient.T * coefficient).I) * coefficient.T
    coefficient_weighted = coefficient_b[half_window]
    coefficient_weighted = coefficient_weighted.T

    data_filtered = []
    for i in range(len(data) - window_size):
        y = [data[i + j] for j in range(window_size)]
        y1 = np.mat(y) * coefficient_weighted
        y1 = float(y1)
        data_filtered.append(y1)

    return data_filtered

# Mean-value Iteration Filter
def mvi(data: list):

    length_data = len(data)
    data = np.array(data)
    data_test = data
    mean = np.zeros((length_data - 2), float)

    for i in range(1, length_data - 1):
        mean[i - 1] = (data[i - 1] + data[i + 1]) / 2
    temp = data[1: length_data - 1]
    delta = np.abs(temp) * 0.1
    delta_i = np.abs(temp - mean)
    judge = delta_i - delta
    max_index = np.where(judge == np.max(judge))
    max_index = max_index[0][0]


    while judge[max_index] > 0:

        data[max_index + 1] = mean[max_index]
        delta[max_index] = np.abs(data[max_index + 1]) * 0.1

        if max_index == 0:
            mean[max_index + 1] = (data[max_index + 1] + data[max_index + 3]) / 2
        elif max_index == length_data - 3:
            mean[max_index - 1] = (data[max_index - 1] + data[max_index + 1]) / 2
        else:
            mean[max_index - 1] = (data[max_index - 1] + data[max_index + 1]) / 2
            mean[max_index + 1] = (data[max_index + 1] + data[max_index + 3]) / 2
        temp = data[1: length_data - 1]
        delta_i = np.abs(temp - mean)


        judge = delta_i - delta
        max_index = np.where(judge == np.max(judge))
        max_index = max_index[0][0]

    return data


# Whittaker Smoother
def ws(data, quality, lamda):


    length_data = len(data)
    data_array = np.array(data)
    d = np.zeros((length_data - 2, length_data), float)
    w = np.zeros((length_data, length_data), float)

    for i in range(length_data):
        if quality[i] == 2:
            w[i, i] = 1
        elif quality[i] == 0:
            w[i, i] = 0
        else:
            w[i, i] = 0.25

    for i in range(length_data - 2):
        d[i, i] = 1
        d[i, i + 1] = -2
        d[i, i + 2] = 1

    z = np.dot(np.linalg.inv(w + lamda * np.dot(d.T, d), ), w.dot(data_array.T))
    return list(z)

