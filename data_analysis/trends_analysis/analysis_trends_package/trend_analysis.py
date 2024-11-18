import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from scipy.signal import argrelextrema
from typing import Generator


def log_results(func):
    """
    Декоратор для логирования выполнения функции.

    Параметры:
    func: Функция, которую нужно обернуть.

    Возвращает:
    Обернутая функция с реализацией логирования.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} completed.")
        return result
    return wrapper


class TrendAnalyzer:
    """
    Класс для анализа временного ряда поисковых трендов.

    Поля класса:
    data (pd.Series): Временной ряд данных, переданный для анализа.
    results (pd.DataFrame): Таблица для хранения результатов анализа.
    """

    def __init__(self, data: pd.Series):
        """
        Инициализация объекта для анализа временного ряда трендов.

        Параметры:
        data (pd.Series): Временной ряд данных.
        """
        self.data = data
        self.results = pd.DataFrame(index=data.index)

    @staticmethod
    @log_results
    def get_trends_data(keywords: list[str], timeframe: str = 'today 5-y', geo: str = '') -> pd.DataFrame:
        """
        Получает данные трендов для заданных ключевых слов с использованием pytrends.

        Параметры:
        keywords (list[str]): Список ключевых слов для поиска.
        timeframe (str): Временной промежуток для получения данных.
        geo (str): Географическая область (по умолчанию пустая строка).

        Возвращает:
        pd.DataFrame: Данные трендов с временными метками.
        """
        pytrends = TrendReq()
        pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo=geo)
        data = pytrends.interest_over_time().drop(columns='isPartial')

        return data

    def moving_average(self, window: int = 3) -> pd.Series:
        """
        Вычисляет скользящее среднее для временного ряда.

        Параметры:
        window (int): Размер окна для скользящего среднего.

        Возвращает:
        pd.Series: Серия с вычисленным скользящим средним.
        """
        self.results['Moving Average'] = self.data.rolling(window=window).mean()
        return self.results['Moving Average']

    def difference(self) -> pd.Series:
        """
        Вычисляет дифференциал временного ряда.

        Возвращает:
        pd.Series: Серия с вычисленным дифференциалом.
        """
        self.results['Differential'] = self.data.diff()
        return self.results['Differential']

    def autocorrelation(self, lag: int = 1) -> float:
        """
        Вычисляет автокорреляцию временного ряда на заданный лаг.

        Параметры:
        lag (int): сдвиг для вычисления автокорреляции.

        Возвращает:
        float: Значение автокорреляции для указанного сдвига.
        """
        return self.data.autocorr(lag)

    def find_extremium_points(self) -> pd.DataFrame:
        """
        Находит локальные максимумы и минимумы во временном ряду.

        Возвращает:
        pd.DataFrame: DataFrame с колонками 'Maximum' и 'Minimum',
        содержащими значения локальных экстремумов.
        """
        maximum = argrelextrema(self.data.values, np.greater)[0]
        minimum = argrelextrema(self.data.values, np.less)[0]

        max_values = []
        min_values = []

        for i in range(len(self.data)):
            if i in maximum:
                max_values.append(self.data.iloc[i])
            else:
                max_values.append(np.nan)

            if i in minimum:
                min_values.append(self.data.iloc[i])
            else:
                min_values.append(np.nan)

        self.results['Maximum'] = pd.Series(max_values, index=self.data.index)
        self.results['Minimum'] = pd.Series(min_values, index=self.data.index)
        return self.results[['Maximum', 'Minimum']]

    @log_results
    def save_to_excel(self, filename: str = "search_trend_analysis_results.xlsx") -> None:
        """
        Сохраняет результаты анализа в Excel файл.

        Параметры:
        filename (str): Имя файла для сохранения.

        """
        self.results = pd.DataFrame ({
            'Moving Average': self.moving_average(),
            'Differential': self.difference(),
            'Autocorrelation': pd.Series([self.autocorrelation(lag=1)] * len(self.data), index=self.data.index),
            'Maximum': self.find_extremium_points()['Maximum'],
            'Minimum': self.find_extremium_points()['Minimum']
        })

        self.results.to_excel(filename)

    @log_results
    def generate_results(self) -> Generator[tuple[str, pd.Series], None, None]:
        """
        Генератор для получения результатов анализа по каждой колонке.

        Возвращает:
        Generator[tuple[str, pd.Series], None, None]: Генератор,
        который поочередно возвращает способ анализа и соответствующий pd.Series.
        """
        analyses = {
            'Moving Average': self.moving_average(),
            'Differential': self.difference(),
            'Autocorrelation': pd.Series([self.autocorrelation(lag=1)] * len(self.data), index=self.data.index),
            'Maximum': self.find_extremium_points()['Maximum'],
            'Minimum': self.find_extremium_points()['Minimum']
        }

        for name, series in analyses.items():
            yield name, series
