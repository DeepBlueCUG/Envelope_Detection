# Bit computation, evaluate the pixel state based on the cloud flag and quality flag
import functions_preprocessing as preprocessing_data
import numpy as np

# Evaluate the state of the pixels (clear, cloudy and shadow or other states), and output
# the number of the duration of the pixel state (clear or cloud-affected).
def count_data_state(cloud_flag: list, qc_flag: list):

    length_data = len(cloud_flag)
    pointer_clear = 0  # The clear pixel pointer, initialized ad 0
    pointer_affected = 0  # The cloud affected pixel pointer, initialized ad 0
    weather = np.zeros((2, length_data), float)

    for i in range(length_data):

        # Recode the cloud grade
        # 1 means clear, cloudy means 2 and 3 means other states
        current_cloud_flag = int(cloud_flag[i])
        current_qc = int(qc_flag[i])
        if current_cloud_flag & 1 == 1:
            cloud_grade = 2
        elif current_cloud_flag & 2 == 2:
            cloud_grade = 3
        elif current_cloud_flag & 3 == 3:
            cloud_grade = 3
        elif current_cloud_flag & 4 == 4:
            cloud_grade = 3
        else:
            cloud_grade = 1

        # recode the quality grade
        if current_qc & 1 == 1:
            quality_grade = 3
        elif current_qc & 2 == 2:
            quality_grade = 2
        elif current_qc & 3 == 3:
            quality_grade = 3
        else:
            quality_grade = 1

        # Evaluate the pixel state based on cloud grade and quality grade
        # Good quality and no cloud cover
        if quality_grade == 1 and cloud_grade == 1:
            state = 1
        # Good quality but cloud cover
        elif quality_grade == 1 and cloud_grade == 2:
            state = 2
        # Bad quality but cloud cover
        elif quality_grade == 2 and cloud_grade == 2:
            state = 2
        # Good quality with shadow
        elif quality_grade == 1 and cloud_grade == 3:
            state = 3
        # Bad quality with shadow
        elif quality_grade == 2 and cloud_grade == 3:
            state = 3
        # Other states
        else:
            state = 3

        if state == 1:
            pointer_clear += 1  # The pixel is not affected
            if pointer_affected != 0:
            # If the pointer_affected is not zero, the change of the pointer_clear means
            # the state of the pixel changes as well. Therefore, output the pointer_affected
            # and reset it.
                weather[1, pointer_affected - 1] += 1
                pointer_affected = 0
        else:
            pointer_affected += 1
            if pointer_clear != 0:
                weather[0, pointer_clear - 1] += 1
                pointer_clear = 0

        if i == length_data - 1 and pointer_clear != 0:
            weather[0, pointer_clear - 1] += 1
        if i == length_data - 1 and pointer_affected != 0:
            weather[1, pointer_affected - 1] += 1

    return weather


# This function has the same principal with count_data_state, and output the proportions
# of the three pixel states
def compute_pixel_state(cloud_name, qc_name):

    cloud_flag = preprocessing_data.read_data_from_excel(cloud_name, 'timeseries', 'quality')
    qc_flag = preprocessing_data.read_data_from_excel(qc_name, 'timeseries', 'quality')

    pixel_state = np.zeros(3, int)


    for i in range(len(cloud_flag)):

        current_cloud_flag = cloud_flag[i]
        current_qc_flag = qc_flag[i]

        for j in range(len(current_cloud_flag)):

            current_cloud = int(current_cloud_flag[j])
            current_qc = int(current_qc_flag[j])
            if current_cloud & 1 == 1:
                cloud_grade = 2
            elif current_cloud & 2 == 2:
                cloud_grade = 3
            elif current_cloud & 3 == 3:
                cloud_grade = 3
            elif current_cloud & 4 == 4:
                cloud_grade = 3
            else:
                cloud_grade = 1

            if current_qc & 1 == 1:
                quality_grade = 3
            elif current_qc & 2 == 2:
                quality_grade = 2
            elif current_qc & 3 == 3:
                quality_grade = 3
            else:
                quality_grade = 1


            if quality_grade == 1 and cloud_grade == 1:
                pixel_state[0] = pixel_state[0] + 1

            elif quality_grade == 1 and cloud_grade == 2:
                pixel_state[1] = pixel_state[1] + 1

            elif quality_grade == 2 and cloud_grade == 2:
                pixel_state[1] = pixel_state[1] + 1

            elif quality_grade == 1 and cloud_grade == 3:
                pixel_state[2] = pixel_state[2] + 1

            elif quality_grade == 2 and cloud_grade == 3:
                pixel_state[2] = pixel_state[2] + 1

            else:
                pixel_state[2] = pixel_state[2] + 1

    output = []
    for item in pixel_state:
        output.append(round(item / pixel_state.sum(), 4))

    return output



# Change the number of the duration of the pixel state (clear or cloud-affected) into the frequency distribution
def operating_probablity_density(weather_count):
    num_clear = 0
    num_effected = 0
    shape_weather_count = weather_count.shape
    for i in range(shape_weather_count[1]):
        num_clear += weather_count[0, i] * (i + 1)
        num_effected += weather_count[1, i] * (i + 1)
    all_number = num_clear + num_effected

    for i in range(shape_weather_count[1]):
        weather_count[0, i] = weather_count[0, i] * (i + 1) / all_number
        weather_count[1, i] = weather_count[1, i] * (i + 1) / all_number
    return weather_count

