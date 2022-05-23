# 大修意见，有人问模拟光滑曲线为什么使用非对称高斯。
# 这里就把模拟数据用非对称高斯解一下，然后把参数在文章里标出
import numpy as np
import matplotlib.pyplot as plt


file_path = "E:\\Envelope_Detection\\code\\"
output_data = file_path + "simulated_real.txt"

simulated_t = np.array(range(1, 201))
x1 = 110
t_left = simulated_t[: x1]
t_right = simulated_t[x1:]
a = 0.2
b = 0.65
x2 = 42
x3 = 2
x4 = 38
x5 = 2.5

fitted_left = []
parameter_left = x1 - t_left
for item in parameter_left:
    fitted = a + b * np.exp(-1 * (item / x2) ** x3)
    fitted_left.append(fitted)

parameter_right = (t_right - x1)
fitted_right = []
for item in parameter_right:
    fitted = a + b * np.exp(-1 * (item / x4) ** x5)
    fitted_right.append(fitted)

fitted_data = fitted_left + fitted_right
# fitted_data = np.array([fitted_data])

plt.plot(fitted_data, ls="-", lw=2, label="Simulated")
plt.show()


line_1 = ''
for item in fitted_data:
    line_1 = line_1 + ' ' + str(item)
with open(output_data, 'w') as file_handle:
    file_handle.write(line_1)
    file_handle.close()