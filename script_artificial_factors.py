import functions_bit_computation as bit_computation
import functions_preprocessing as preprocessing
import functions_simulation as simulation
import functions_reconstruction as reconstruction
import functions_evaluation_index as evaluation_index
import numpy as np
import random
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
# The duration of long gap
artifical_factors = [10, 20, 30, 60, 90]
# The rate of high value
# artifical_factors = [0.03, 0.05, 0.1, 0.15, 0.2]
noise_random = 0.05
noise_subpixel = 0.05
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
ac_array = np.zeros((len(method_list), len(artifical_factors)), float)# record the mean of ac

# pixel_state includes "clear", "cloud cover" and "shadows and other states".
pixel_state = bit_computation.compute_pixel_state(file_path + 'cloud_timeseries.xls', file_path + 'cloud_timeseries.xls')
cloudcover_rate = pixel_state[1] / (pixel_state[1] + pixel_state[2])
shadow_rate = 1 - cloudcover_rate

for i in range(len(artifical_factors)):
    for repeat in range(repetition):


        ac_list = []

        # Creat simulated quality band
        simulated_quality = simulation.create_simulate_quality(probability_density, cloudcover_rate)
        # Add artificial noises
        simulated_observation = simulation.create_simulate_data\
            (simulated_actual, simulated_quality, integral_cloud, noise_random, noise_subpixel)

        # Add artificial long-gap
        missingdata_start = random.randint(30, len(simulated_quality) - (20 + artifical_factors[i]))#缺失数起始位置
        for j in range(missingdata_start, missingdata_start + artifical_factors[i]):

            random_cloud = random.random()
            ndvi_cloud = simulation.__read_cloud_ndvi(integral_cloud, random_cloud)

            simulated_quality[j] = 0
            simulated_observation[j] = ndvi_cloud

        # # high-value outliers
        # high_value_num = int(len(simulated_observation) * artifical_factors[i])
        # high_value_index = random.sample(range(len(simulated_observation)), high_value_num)
        # for index in high_value_index:
        #     simulated_quality[index] = 2  # 高值噪声要参与运算的
        #     simulated_observation[index] = random.uniform(simulated_actual[index], 1)

        # SG filtering, HANTS and WS need masked bad quality data based on simulated quality band
        value_effective = [simulated_observation[0]]
        t_effective = [1]
        for j in range(1, len(simulated_observation) - 1):
            if simulated_quality[j] == 2:
                value_effective.append(simulated_observation[j])
                t_effective.append(j + 1)
        value_effective.append(value_effective[-1])
        t_effective.append(len(simulated_observation))
        t_new = range(1, len(simulated_observation) + 1)

        linear_interpolate = interpolate.interp1d(t_effective, value_effective, kind="slinear")
        value_effective_interpolated = linear_interpolate(t_new)
        data_sg = reconstruction.sg_filtering(value_effective_interpolated, half_window, 3)

        hants = reconstruction.hants(hants_order)
        data_hants = hants.hants(value_effective, t_effective, t_new)
        data_hants_sg = reconstruction.sg_filtering(data_hants, half_window, 3)
        data_hants = data_hants[half_window: len(data_hants) - half_window - 1]  # Unite the length of the data


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
        ac_list.append(evaluation_index.ac(simulated_actual_show, data_bise_sg))
        ac_list.append(evaluation_index.ac(simulated_actual_show, data_ed_sg))
        ac_list.append(evaluation_index.ac(simulated_actual_show, data_ws))
        ac_list.append(evaluation_index.ac(simulated_actual_show, data_mvi_sg))


        for j in range(len(ac_list)):
            ac_array[j][i] = ac_array[j][i] + ac_list[j]


    for j in range(len(method_list)):
        ac_array[j][i] = ac_array[j][i] / repetition


for i in range(len(method_list)):
    print(method_list[i])
    print(ac_array[i])




