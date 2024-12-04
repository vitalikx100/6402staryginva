import threading
import logging
import time
import pandas as pd
from data_analysis.get_trends_data import TrendsData
from data_analysis.trends_analysis.analysis_trends_package.trend_analysis import TrendAnalyzer


class TrendsMonitoring(threading.Thread):
    """
    Класс для мониторинга трендов, работающий в отдельном потоке.

    Поля класса:
    trends_data (TrendsData): Объект TrendsData для получения данных трендов.
    time_delay (int): Интервал времени в секундах между запусками мониторинга.
    is_active (Bool): флаг для регулирования выполнения мониторинга потоком
    logger: Логгер для записи информации о процессе мониторинга.
    """

    def __init__(self, trends_data: TrendsData, time_delay: int = 60):
        """
        Инициализация объекта TrendsMonitoring.

        Параметры:
        trends_data (TrendsData): Объект TrendsData для получения данных трендов.
        time_delay (int): Интервал времени между запусками мониторинга.
        """
        super().__init__()
        self.trends_data = trends_data
        self.time_delay = time_delay
        self.is_active = True
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Метод, который выполняется при запуске потока.
        Обрабатывает полученные данные раз в задержку времени.
        """
        self.logger.info("Trends monitoring started.")
        while self.is_active:
            try:
                data = self.trends_data.fetch_data()
                data_series = data.iloc[:, 0]
                analyzer = TrendAnalyzer(data_series)
                results = analyzer.generate_results()
                if results:
                    results_dict = {}
                    for name, series in results:
                        results_dict[name] = series
                    results_df = pd.DataFrame(results_dict, index=data_series.index)
                    self.logger.info("Generated results successfully.")
                    print(results_df)
                time.sleep(self.time_delay)
            except Exception as e:
                self.logger.error(f"Error monitoring data: {e}")
                self.is_active = False
                raise

    def stop(self):
        """Останавливает выполнение потока."""

        self.is_active = False
        super().join(timeout=None)
        self.logger.info("Monitoring service OFF")
