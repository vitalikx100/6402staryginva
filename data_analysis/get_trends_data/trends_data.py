import logging
from pytrends.request import TrendReq
import pandas as pd


class TrendsData:
    """
    Класс для работы с данными трендов.

    Поля класса:
    keywords (list[str]): Список ключевых слов для анализа.
    timeframe (str): Временной промежуток для получения данных.
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
        self.keywords = keywords
        self.timeframe = timeframe
        self.geo = geo
        self.logger = logging.getLogger(__name__)

    def fetch_data(self) -> pd.DataFrame:
        """
        Получает данные трендов на основе параметров экземпляра с использованием pytrends

        Возвращает:
        pd.DataFrame: Данные трендов с временными метками.
        """
        try:
            pytrends = TrendReq()
            pytrends.build_payload(kw_list=self.keywords, timeframe=self.timeframe, geo=self.geo)
            data = pytrends.interest_over_time().drop(columns='isPartial')

            if data.empty:
                self.logger.warning("No data fetched for the given keywords.")
                return pd.DataFrame()
            return data

        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            raise
