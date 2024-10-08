import numpy as np
import yaml

#функция считывания данных с файла
def read_file(file):
    with open(file, 'r') as file:
        params = yaml.safe_load(file)
    return params

#реализация расчета фукнции
def function(x, a, b, c):
    return np.abs(a * np.exp(1j * b * x + c))**2

#считываем параметры с файла config.yaml
#записываем в переменную params
params = read_file('config.yaml')

#запись значений в переменные
n0 = params['n0']
h = params['h']
nk = params['nk']
a = params['a']
b = params['b']
c = params['c']

#формируем значения x в зависимости от диапазона и шага
x_values = np.arange(n0, nk + h, h)

#Вычисление значений функции
y_values = function(x_values, a, b, c)

#Запись результатов в results.txt
with open('results.txt', 'w') as f:
    for x, y_val in zip(x_values, y_values):
        f.write(f'{x}, {y_val}\n')