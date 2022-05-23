# Compute the frequency distribution (probability) of the duration of the pixel state
# (clear or cloud-affected) from qc and cloud flags time-series
# The simulated quality band is generated based on this frequency distribution.

import functions_preprocessing as preprocessing_data
import functions_bit_computation as bit_computation
import functions_postprocessing as postprocessing_data


file_path = "E:\\Envelope_Detection\\code\\"
output_data = 'E:\\Envelope_Detection\\code\\probablity_density.txt'



original_cloud_name = file_path + "cloud_timeseries.xls"
cloud = preprocessing_data.read_data_from_excel(original_cloud_name, 'timeseries', 'quality')

original_qc_name = file_path + "qc_timeseries.xls"
qc = preprocessing_data.read_data_from_excel(original_qc_name, 'timeseries', 'quality')

for j in range(len(cloud)):

    current_cloud = cloud[j]
    current_qc = qc[j]

    # exclude null value in the time-series
    cloud_filtered = []
    qc_filtered = []
    for index in range(len(current_cloud)):
        if current_cloud[index] != '':
            cloud_filtered.append(current_cloud[index])
            qc_filtered.append(current_qc[index])

    weather = bit_computation.count_data_state(current_cloud, current_qc)
    if j == 0:
        weather_count = weather
    else:
        weather_count = weather_count + weather


probability_density = bit_computation.operating_probablity_density(weather_count)
postprocessing_data.plot_data(probability_density[:, :50])

probability_density_list = probability_density.tolist()
line_1 = ''
line_2 = ''
for item in probability_density_list[0]:
    line_1 = line_1 + ' ' + str(round(item, 6))
for item in probability_density_list[1]:
    line_2 = line_2 + ' ' + str(round(item, 6))
with open(output_data, 'w') as file_handle:
    file_handle.write(line_1)
    file_handle.write('\n')
    file_handle.write(line_2)
    file_handle.close()










