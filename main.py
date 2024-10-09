import numpy as np
import yaml
import argparse


def read_file(file: str) -> dict[str, float]:
    '''
     Данная функция считывает файл.
     file принимает строковое значение, представляющее собой имя файла
     и возвращает словарь со строковым ключом и значением типа число с плавающей точкой (float).
    '''
    with open(file, 'r') as file:
        params = yaml.safe_load(file)
    return params

def calculate_y(params: dict[str, float]) -> None :
    '''
     Вычисление значения функции.
     params принимает словарь со строковым ключом и значением с типом плавающая точка (float).
    '''
    x_value = params['n0']
    y_values = []
    while x_value <= params['nk']:
        exponenta = np.exp(1j * params['b'] * x_value + params['c'])
        y_value = np.abs((params['a'] * exponenta)**2)
        y_values.append(y_value)
        x_value += params['h']
    with open('results.txt', 'w') as file:
        for y_value in y_values:
            file.write(f'y: , {y_value}\n')

def parse_args(params: dict[str, float]) -> float:
    '''
     params принимает словарь со строковым ключом и значением с типом плавающая точка (float)
     Результат работы функции возвращает значение с типом плавающая точка (float)
    '''
    parser = argparse.ArgumentParser(description='Вычисление значения функции')
    parser.add_argument('n0', type=float, nargs="?")
    parser.add_argument('h', type=float, nargs="?")
    parser.add_argument('nk', type=float, nargs="?")
    parser.add_argument('a', type=float, nargs="?")
    parser.add_argument('b', type=float, nargs="?")
    parser.add_argument('c', type=float, nargs="?")
    args = parser.parse_args()

    for key, value in args._get_kwargs():
        if value is not None:
            params[key] = value
    calculate_y(params)

if __name__ == '__main__':
    params = read_file('config.yaml')
    calculate_y(params)
    params = parse_args(params)