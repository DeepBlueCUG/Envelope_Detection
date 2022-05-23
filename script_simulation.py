import functions_bit_computation as bit_computation
import functions_preprocessing as preprocessing
import functions_simulation as simulation
import functions_reconstruction as reconstruction
import functions_evaluation_index as evaluation_index
import numpy as np
from scipy import interpolate


# The script of the simulation

# Parameters of the reconstruction methods
rct = 60  # Attenuation parameter (sigma) of ED-SG
half_window = 10  # Half window size of SG filter
order = 3  # Three order polynomial for SG filter
window_size = half_window * 2 + 1
hants_order = 15  # The number of harmonic waves
ws_lamda = 2.5  # smoothing parameter (lambda) for WS filter
method_list = ['original', 'sg', 'hants', 'bise', 'ed_sg', 'ws', 'mvi']
file_path = 'E:\\Envelope_Detection\\code\\'


# Input simulated real NDVI timeseries
simulated_actual = preprocessing.real_read_in(file_path + 'simulated_real.txt')
# Input the frequency distribution of the duration of the pixel state
probability_density = preprocessing.probability_density_read_in(file_path + 'probablity_density.txt')
# Input the frequency distribution of cloud covered NDVI values
cloud_density = preprocessing.cloud_density_read_in(file_path + 'cloudcover_ndvi.txt')
# repetition of the experiment
repetition = 1

# compute the probability of the NDVI
integral_cloud = simulation.integral_cloud_ndvi(cloud_density)
overall_ac = np.zeros((len(method_list), repetition), float)
overall_variance = np.zeros((len(method_list), repetition), float)
ac_mean = np.zeros((len(method_list), 21, 21), float)  # record the mean of ac

# pixel_state includes "clear", "cloud cover" and "shadows and other states".
pixel_state = bit_computation.compute_pixel_state(file_path + 'cloud_timeseries.xls', file_path + 'cloud_timeseries.xls')
cloudcover_rate = pixel_state[1] / (pixel_state[1] + pixel_state[2])
shadow_rate = 1 - cloudcover_rate

for repeat in range(repetition):

    print('Repeation: ', repeat)
    ac_array = np.zeros((len(method_list), 21, 21), float)

    for i in range(21):

        for j in range(21):

            noise_random = 0.01 * i
            noise_subpixel = 0.01 * j


            ac_list = []

            # Creat simulated quality band
            simulated_quality = simulation.create_simulate_quality(probability_density, cloudcover_rate)
            # Add artificial noises
            simulated_observation = simulation.create_simulate_data\
                (simulated_actual, simulated_quality, integral_cloud, noise_random, noise_subpixel)

            # The performances of SG, HANTS and WS depend on the precision of the quality band. Here we randomly add
            # to the quality band to test the algorithms
            # pixel_state = bit_operation.compute_pixel_state(file_path + 'cloud_timeseries.xls', file_path + 'cloud_timeseries.xls')
            # cloudcover_rate = pixel_state[1] / (pixel_state[1] + pixel_state[2])
            # shadow_rate = 1 - cloudcover_rate
            # error_rate = 0.1
            # for k in range(len(simulated_quality)):
            #     random_value = random.uniform(0, 1)
            #     if random_value <= 1 - error_rate:
            #         if simulated_quality[k] == 2:
            #             # simulated_quality[k] = 1
            #             random_cloud = random.uniform(0, 1)
            #             if random_cloud < cloudcover_rate:
            #                 simulated_quality[k] = 0  # 云遮盖
            #             else:
            #                 simulated_quality[k] = 1  # 云阴影
            #         else:
            #             simulated_quality[k] = 2

            # SG filtering, HANTS and WS need masked bad quality data based on simulated quality band
            value_effective = [simulated_observation[0]]
            t_effective = [1]
            for k in range(1, len(simulated_observation) - 1):
                if simulated_quality[k] == 2:
                    value_effective.append(simulated_observation[k])
                    t_effective.append(k + 1)
            value_effective.append(value_effective[-1])
            t_effective.append(len(simulated_observation))
            t_new = range(1, len(simulated_observation) + 1)

            linear_interpolate = interpolate.interp1d(t_effective, value_effective, kind="slinear")
            value_effective_interpolated = linear_interpolate(t_new)
            data_sg = reconstruction.sg_filtering(value_effective_interpolated, half_window, 3)
            #
            hants = reconstruction.hants(hants_order)
            data_hants = hants.hants(value_effective, t_effective, t_new)
            data_hants_sg = reconstruction.sg_filtering(data_hants, half_window, 3)
            data_hants = data_hants[half_window: len(data_hants) - half_window - 1]  # Unite the length of the data

            # data_idr = filtering_data.idr(simulated_observation)
            # data_idr_sg = filtering_data.sg_filtering(data_idr, half_window, 3)
            # data_idr = data_idr[half_window: len(data_idr) - half_window - 1]

            data_bise = reconstruction.bise(simulated_observation, 20, 0.1, 0.2)
            data_bise_sg = reconstruction.sg_filtering(data_bise, half_window, 3)
            data_bise = data_bise[half_window: len(data_bise) - half_window - 1]

            data_envelope_detection = reconstruction.envelope_detection(simulated_observation, t_new, rct)
            data_ed_sg = reconstruction.sg_filtering(data_envelope_detection, half_window, 3)
            data_envelope_detection = data_envelope_detection[
                                      half_window: len(data_envelope_detection) - half_window - 1]

            data_ws = reconstruction.ws(simulated_observation, simulated_quality, ws_lamda)
            data_ws_sg = reconstruction.sg_filtering(data_ws, half_window, order)
            data_ws = data_ws[half_window: len(data_ws) - half_window - 1]

            data_mvi = reconstruction.mvi(simulated_observation)
            data_mvi_sg = reconstruction.sg_filtering(data_mvi, half_window, 3)
            data_mvi = data_mvi[half_window: len(data_mvi) - half_window - 1]

            simulated_actual_show = simulated_actual[
                                      half_window: len(simulated_actual) - half_window - 1]

            ac_list.append(evaluation_index.ac(simulated_actual, simulated_observation))
            simulated_observation = simulated_observation[half_window: len(simulated_observation) - half_window - 1]
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_sg))
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_hants))
            # ac_list.append(evaluation_index.ac(simulated_actual_show, data_idr_sg))
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_bise_sg))
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_ed_sg))
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_ws))
            ac_list.append(evaluation_index.ac(simulated_actual_show, data_mvi_sg))


            for k in range(len(ac_list)):
                ac_array[k, i, j] = ac_array[k, i, j] + ac_list[k]


            # simulated_observation = simulated_observation[half_window: len(simulated_observation) - half_window - 1]
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_sg))
            # print('sg')
            # postprocessing_data.plot_data(data_output)
            # #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_hants, data_hants_sg))
            # print('hants')
            # postprocessing_data.plot_data(data_output)
            #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_idr, data_idr_sg))
            # print('idr')
            # postprocessing_data.plot_data(data_output)
            #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_bise, data_bise_sg))
            # print('bise')
            # postprocessing_data.plot_data(data_output)
            #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_envelope_detection, data_ed_sg))
            # print('ed')
            # postprocessing_data.plot_data(data_output)
            #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_ws, data_ws_sg))
            # print('ws')
            # postprocessing_data.plot_data(data_output)
            #
            # data_output = np.array(simulated_observation)
            # data_output = np.row_stack((data_output, simulated_actual_show, data_mvi, data_mvi_sg))
            # print('mvi')
            # postprocessing_data.plot_data(data_output)

    for i in range(len(method_list)):
        overall_ac[i][repeat] = ac_array[i].mean()
        overall_variance[i][repeat] = ac_array[i].var()
        ac_mean[i] = ac_mean[i] + ac_array[i]



ac_mean = ac_mean / repetition
for i in range(len(method_list)):
    print(method_list[i])
    print(overall_ac[i].mean())
    print(overall_variance[i].mean())


# Output AC array
ac_mean = ac_mean.tolist()
index = 0
for method in method_list:

    method_ac = ac_mean[index]
    ac_list = []
    # 将数据字符串化
    for item in method_ac:
        ac_string = ''
        for i in range(len(item)):
            ac_string = ac_string + ' ' + str(item[i])
        ac_list.append(ac_string)
    index += 1

    headline = "\t"
    output_name = file_path + method + '.txt'
    # with open(output_name, 'w') as file_handle: #以w格式打开之后直接关闭会会清除文本文件内容
    #     file_handle.close()
    with open(output_name, 'a') as file_handle:  # .txt可以不自己新建,代码会自动新建
        for line in ac_list:
            file_handle.write(line)
            file_handle.write('\n')
        file_handle.close()

