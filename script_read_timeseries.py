# Extract data points and time from the original CSV files downloaded from GEE
# and write the timeseries into a excel sheet
import csv
import xlwt

file_path = "E:\\Envelope_Detection\\code\\"
filename = "ndvi_test.csv"  # input file must be csv file
output_filename = "ndvi_timeseries.xls"  # output file  should be xls file

def write_sheet(data, sheet_name, output_filename):
    output_length = len(data)

    sheet = workbook.add_sheet(sheet_name)
    for i in range(output_length):
        output_string = data[i]
        output_split = output_string.split(',')
        output_float = []
        # num = 0
        for item in output_split:
            # num = num + 1
            # print(i)
            # print(num)
            if item.strip() == 'null':
                output_float.append(None)
            else:
                output_float.append(float(item))
        for j in range(len(output_float)):
            sheet.write(j, i, output_float[j])
    workbook.save(output_filename)


timeseries = []
time = []
workbook = xlwt.Workbook()
with open(file_path + filename, 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    column_timeseries = [row['property_timeseries_name'] for row in reader]
    csvfile.close()
with open(file_path + filename, 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    column_time = [row['property_time_name'] for row in reader]
    csvfile.close()

# eliminate square brackets of the data
for j in range(len(column_timeseries)):
    column_substring = column_timeseries[j][1:len(column_timeseries[j]) - 1]
    timeseries.append(column_substring)
for j in range(len(column_time)):
    column_substring = column_time[j][1:len(column_time[j]) - 1]
    time.append(column_substring)


write_sheet(timeseries, 'timeseries', file_path + output_filename)
write_sheet(time, 'time', file_path + output_filename)