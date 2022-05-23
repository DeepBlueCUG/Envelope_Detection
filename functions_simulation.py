#进行生成模拟数据
import random
import numpy as np

# Some functions necessary in the script_simulation


# Creat the simulated quality band based on the frequency distribution of the pixel sate
# If the pixel is affected by the cloud, the state can be divided in to "cloudy" and "shadow and
# other state", "probability_cloud" means the probability of the "cloudy", which can be computed
# by the function "compute_pixel_state" in "functions_bit_computation"
def create_simulate_quality(probability_density, probability_cloud):

    probability_density = probability_density.tolist()
    good_probability_density = probability_density[0]
    bad_probability_density = probability_density[1]
    length_data = 200  # length of the quality band
    state = 2  # 2 means the pixel is clear, 1 means the pixel is affected by clouds
    duration = 1  # The duration of the status
    quality = [2]  # The value of the quality flag, 0 means cloudy, 1 means shadow or other states, 2 means clear
    # These quality flags are used to compute Eq.(8) in the paper, which is different with the variate "state"


    for i in range(1, length_data):
        # For instance, if the "state = 1" of the pixel doesn't last 2 days, that means the state in the second day
        # covers to "2"
        if state == 1:
            random_index = random.random()
            # Compare random_index with bad_probability_density to figure out the state remains 1 or be update to 2
            if random_index < bad_probability_density[duration - 1] / (bad_probability_density[duration - 1]
                                                                       + good_probability_density[0]):
                # The state value remains 1
                # Further decide the quality is "cloudy" or "shadow or other state"
                random_cloud = random.uniform(0, 1)
                if random_cloud < probability_cloud:
                    quality.append(0)  # "cloudy"
                else:
                    quality.append(1)  # "shadow or other state"
                duration = duration + 1
            else:
                # update the sate into 2, the quality flag is 2 (clear)
                state = 2
                quality.append(2)
                duration = 1

        else:
            random_index = random.random()
            if random_index < good_probability_density[duration - 1] / (good_probability_density[duration - 1]
                                                                        + bad_probability_density[0]):
                # state value remains 2, the quality flag is 2 (clear)
                quality.append(2)
                duration = duration + 1
            else:
                # update the sate into 1
                state = 1
                random_cloud = random.random()
                if random_cloud < probability_cloud:
                    quality.append(0)  # "cloudy"
                else:
                    quality.append(1)  # "shadow or other state"
                duration = duration + 1

    return quality


# integral the frequency distribution of NDVI values to compute the probability of the NDVI
def integral_cloud_ndvi(cloud_density):

    ndvi = cloud_density[0][:]
    frequency = cloud_density[1][:]

    frequency_integral = np.zeros((2, len(frequency)))
    frequency_integral[0][0] = ndvi[0]
    frequency_integral[1][0] = frequency[0]
    for i in range(1, len(ndvi)):
        frequency_integral[0][i] = ndvi[i]
        frequency_integral[1][i] = frequency_integral[1][i - 1] + frequency[i]

    return frequency_integral


# Check the probability of a certain NDVI
def __read_cloud_ndvi(frequency_integral, random_cloud):
    ndvi = frequency_integral[0][:]
    frequency = frequency_integral[1][:]
    simulated_ndvi = 0

    for i in range(len(ndvi)):
        if random_cloud > frequency[i]:
            continue
        else:
            if i == 0:
                simulated_ndvi = random.uniform(0, ndvi[i])
            elif i == len(ndvi) - 1:
                simulated_ndvi = random.uniform(ndvi[i], ndvi[len(ndvi) - 1])
            else:
                simulated_ndvi = random.uniform(ndvi[i - 1], ndvi[i])
            break

    return simulated_ndvi



def create_simulate_data(data, quality, frequency_integral, noise_random, noise_subpixel):
    # data: simulated smooth NDVI timeseries
    # quality: simulated quality band
    # frequency_integral: probability of the cloudy NDVI value
    # noise_random: random noises
    # noise_subpixel: subpixel noise

    length_data = len(data)
    simulated_data = []

    for i in range(length_data):

        if quality[i] == 0 or quality[i] == 1:
            random_cloud = random.random()
            random_cloud_shadow = random.random()
            ndvi_cloud = __read_cloud_ndvi(frequency_integral, random_cloud)
            while ndvi_cloud >= data[i]:
                random_cloud = random.random()
                ndvi_cloud = __read_cloud_ndvi(frequency_integral, random_cloud)
            simulated_observation = (1 - quality[i]) * ndvi_cloud + quality[i] * random_cloud_shadow * data[i]
            simulated_data.append(simulated_observation)
        else:
            random_noise = random.uniform(-1 * noise_random, noise_random)
            subpixel_noise = random.uniform(0, noise_subpixel)
            simulated_data.append(data[i] + random_noise - subpixel_noise)

    return simulated_data