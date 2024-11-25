import logging
from pytrends.request import TrendReq
import pandas as pd
from data_analysis.trends_analysis.analysis_trends_package.trend_analysis import TrendAnalyzer


class TrendsData(TrendAnalyzer):
    """
    Класс для работы с данными трендов.

    Поля класса:
    keywords (list[str]): Список ключевых слов для анализа.
    timeframe (str): Временной промежуток для получения данных (например, 'today 5-y').
    geo (str): Географическая область (по умолчанию пустая строка, что означает глобальный запрос).
    logger: Логгер для записи о процессе получения данных.
    """

    def __init__(self, keywords: list[str], timeframe: str = 'today 5-y', geo: str = ''):
        """
        Инициализация объекта TrendsData.

        Параметры:
        keywords (list[str]): Список ключевых слов для анализа.
        timeframe (str): Временной промежуток для получения данных (по умолчанию 'today 5-y').
        geo (str): Географическая область.
        """
        super().__init__(pd.Series(dtype=float))  # Передаем пустую серию в родительский класс
        self.keywords = keywords
        self.timeframe = timeframe
        self.geo = geo
        self.logger = logging.getLogger(__name__)

    def fetch_data(self) -> pd.DataFrame:
        """
        Получает данные трендов на основе параметров экземпляра с использованием pytrends
        и обрабатывает полученные данные с помощью метода generate_results.

        Возвращает:
        pd.DataFrame: Данные трендов с временными метками.
        """
        self.logger.info(f"Fetching data for keywords: {self.keywords}, timeframe: {self.timeframe}, geo: {self.geo}")
        try:
            pytrends = TrendReq()
            pytrends.build_payload(kw_list=self.keywords, timeframe=self.timeframe, geo=self.geo)
            data = pytrends.interest_over_time().drop(columns='isPartial')

            if data.empty:
                self.logger.warning("No data fetched for the given keywords.")
                return pd.DataFrame()

            self.data = data.iloc[:, 0]
            results = self.generate_results()


            results_dict = {}
            for name, series in results:
                results_dict[name] = series
            results_df = pd.DataFrame(results_dict, index=self.data.index)

            self.logger.info("Generated results successfully.")
            return results_df

        except Exception as e:
            self.logger.warning(f"Error fetching data: {e}")
            raise
