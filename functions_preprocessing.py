# Some data preprocessing functions
import numpy as np
import xlrd
from scipy import interpolate


def real_read_in(filename):

    file_hypothetical_data = open(filename, "r")
    lines_read_in = file_hypothetical_data.readlines()
    lines_split = lines_read_in[0].split(' ')
    data_preprocess = []
    for item in lines_split:
        if item != '':
            data_preprocess.append(float(item))

    return data_preprocess


def probability_density_read_in(filename):

    file_quality = open(filename)
    lines_read_in = file_quality.readlines()
    lines_split_0 = lines_read_in[0].split(' ')
    lines_split_1 = lines_read_in[1].split(' ')
    quality_good = []
    quality_bad = []
    for item in lines_split_0:
        if item != '' and item != '\n':
            quality_good.append(float(item))
    for item in lines_split_1:
        if item != '' and item != '\n':
            quality_bad.append(float(item))

    data_output = np.array(quality_good)
    data_output = np.row_stack((data_output, quality_bad))

    return data_output


def cloud_density_read_in(filename):

    file_quality = open(filename)
    lines_read_in = file_quality.readlines()
    lines_split_0 = lines_read_in[0].split(' ')
    lines_split_1 = lines_read_in[1].split(' ')
    ndvi = []
    probablity = []
    for item in lines_split_0:
        if item != '' and item != '\n':
            ndvi.append(float(item))
    for item in lines_split_1:
        if item != '' and item != '\n':
            probablity.append(float(item))

    data_output = np.array(ndvi)
    data_output = np.row_stack((data_output, probablity))

    return data_output


def read_data_from_excel(data_file_path, sheet_name, tag):

    workBook = xlrd.open_workbook(data_file_path);

    selected_timeseries = []
    #sheet_names = workBook.sheet_names()
    sheet_content = workBook.sheet_by_name(sheet_name);
    for i in range(sheet_content.ncols):
        current_timeseries = sheet_content.col_values(i)
        # selected_timeseries.append(current_timeseries)

        timeseries_folat = []

        if tag == 'ndvi':
            x_axis = []
            # Interpolate the timeseries to fill the empty data
            for j in range(len(current_timeseries)):
                if current_timeseries[j] != '':
                    timeseries_folat.append(current_timeseries[j])
                    x_axis.append(j)
            linear_interploate = interpolate.interp1d(x_axis, timeseries_folat, kind="slinear")
            x_new = range(len(current_timeseries))
            linear_interpolated = linear_interploate(x_new)
            selected_timeseries.append(list(linear_interpolated))

        if tag == 'quality':
            # For quality data, the empty data will be replaced by last data
            for j in range(len(current_timeseries)):
                if current_timeseries[j] == '':
                    timeseries_folat.append(timeseries_folat[-1])
                else:
                    timeseries_folat.append(current_timeseries[j])
            selected_timeseries.append(timeseries_folat)

        if tag == 'time':
            for j in range(len(current_timeseries)):
                timeseries_folat.append(current_timeseries[j])
            selected_timeseries.append(timeseries_folat)

    return selected_timeseries



# def quality_evaluation(cloud_flag: list, qc: list):
#
#     length_data = len(cloud_flag)
#     quality_tag = []
#
#     for i in range(length_data):
#
#         #云波段按位运算并重编码
#         current_cloud_flag = int(cloud_flag[i])
#         current_qc = int(qc[i])
#         if current_cloud_flag & 4 == 4:
#             cloud_grade = 2
#         elif current_cloud_flag & 1 == 1:
#             cloud_grade = 3
#         elif current_cloud_flag & 2 == 1:
#             cloud_grade = 3
#         elif current_cloud_flag & 3 == 1:
#             cloud_grade = 3
#         elif current_cloud_flag == 0:
#             cloud_grade = 0
#         else:
#             cloud_grade = 1
#
#         # 云波段按位运算并重编码
#         if current_qc & 1 == 1:
#             quality_grade = 2
#         elif current_qc & 2 == 1:
#             quality_grade = 2
#         elif current_qc & 3 == 1:
#             quality_grade = 2
#         elif current_qc == 0:
#             quality_grade = 0
#         else:
#             quality_grade = 1
#
#         #根据掩膜情况为当前天气贴状态标签
#         if quality_grade == 1 and cloud_grade == 1:
#             quality_tag.append(1)
#         elif quality_grade == 1 and cloud_grade == 2:
#             quality_tag.append(2)
#         elif quality_grade == 0 and cloud_grade == 0:
#             quality_tag.append(0)
#         else:
#             quality_tag.append(3)
#
#     return quality_tag





