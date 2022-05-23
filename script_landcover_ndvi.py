# Compute the frequency distribution of cloud covered NDVI values based on the cloud flags
# based on this frequency distribution, we can simulate the NDVI values that the pixels were
# covered by cloud.

import functions_preprocessing as preprocessing_data
import numpy as np


file_path = "E:\\Envelope_Detection\\code\\"

# Calibrate the time of NDVI timeseries and cloud flag timeseries. These two timeseries
# should have the same time tags
def time_calibration(time, data, standard_time):
    result = []
    index_t = 0
    for t in range(len(time)):
        if time[t] == standard_time[index_t]:
            result.append(data[t])
            index_t += 1
            if index_t >= len(standard_time):
                break
    return result


ndvi_count = np.zeros(201, dtype=float)  # Recorde the number
ndvi_index = np.zeros(201, dtype=float)  # NDVI value
for i in range(len(ndvi_index)):
    ndvi_index[i] = -1 + 0.01 * i
count = 0  # Total number of the pixels


ndvi_timeseries_name = file_path + "ndvi_timeseries.xls"
timeseries = preprocessing_data.read_data_from_excel(ndvi_timeseries_name, 'timeseries', 'ndvi')
time = preprocessing_data.read_data_from_excel(ndvi_timeseries_name, 'time', 'time')

cloud_timeseries_name = file_path + "cloud_timeseries.xls"
cloud = preprocessing_data.read_data_from_excel(cloud_timeseries_name, 'timeseries', 'quality')
cloud_time = preprocessing_data.read_data_from_excel(cloud_timeseries_name, 'time', 'time')

qc_timeseries_name = file_path + "qc_timeseries.xls"
qc = preprocessing_data.read_data_from_excel(qc_timeseries_name, 'timeseries', 'quality')
qc_time = preprocessing_data.read_data_from_excel(qc_timeseries_name, 'time', 'time')

# clear_result = []
# clear_result_time = []
# effected_result = []
# effected_result_time = []
# print("Original with record")

for i in range(len(timeseries)):
    current_timeseries = timeseries[i]
    current_time = time[i]
    current_cloud = cloud[i]
    current_cloud_time = cloud_time[i]


    time_union = list(set(current_time) & (set(current_cloud_time) ))
    time_union.sort()
    timeseries_filtered = time_calibration(current_time, current_timeseries, time_union)
    cloud_filtered = time_calibration(current_cloud_time, current_cloud, time_union)


    for j in range(len(timeseries_filtered)):

        if timeseries_filtered[j] == '':
            continue

        count += 1
        if int(cloud_filtered[j]) & 1 == 1:

            ndvi = int(timeseries_filtered[j] * 100 + 0.5) / 100.
            index = int((ndvi + 1) * 100)
            ndvi_count[index - 1] = ndvi_count[index - 1] + 1

# Write the frequency distribution of NDVI values
print(count)
ndvi_count = ndvi_count / count
ndvi_count_list = ndvi_count.tolist()
ndvi_index_list = ndvi_index.tolist()
index_string = ''
ndvi_string = ''
for i in range(len(ndvi_index_list)):
    index_string = index_string + ' ' + str(round(ndvi_index_list[i], 2))
    ndvi_string = ndvi_string + ' ' + str(round(ndvi_count_list[i], 4))

headline = "\t"
output_name = file_path + 'cloudcover_ndvi.txt'

with open(output_name, 'w') as file_handle:
    file_handle.write(index_string)
    file_handle.write('\n')
    file_handle.write(ndvi_string)
    file_handle.close()





