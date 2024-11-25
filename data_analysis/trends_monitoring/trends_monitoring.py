import threading
import logging
import time
from data_analysis.get_trends_data import TrendsData


class TrendsMonitoring(threading.Thread):
    """
    Класс для мониторинга трендов, работающий в отдельном потоке.

    Поля класса:
    trends_data (TrendsData): Объект TrendsData для получения данных трендов.
    interval (int): Интервал времени в секундах между запусками fetch_data.
    is_active (Bool): флаг для регулирования выполнения мониторинга потоком
    logger: Логгер для записи информации о процессе мониторинга.
    """

    def __init__(self, trends_data: TrendsData, time_delay: int = 60):
        """
        Инициализация объекта TrendsMonitoring.

        Параметры:
        trends_data (TrendsData): Объект TrendsData для получения данных трендов.
        interval (int): Интервал времени между запусками fetch_data.
        """
        super().__init__()
        self.trends_data = trends_data
        self.time_delay = time_delay
        self.is_active = True
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Метод, который выполняется при запуске потока.
        Периодически вызывает fetch_data, пока не будет установлен флаг остановки.
        """
        self.logger.info("Trends monitoring started.")
        while self.is_active:
            try:
                results = self.trends_data.fetch_data()
                if not results.empty:
                    print(results)
                time.sleep(self.time_delay)
            except Exception as e:
                self.logger.warning(f"Error data fetching: {e}")
                self.is_active = False

    def stop(self):
        """
        Останавливает выполнение потока.
        """
        self.is_active = False
        self.logger.info("Stopping trends monitoring service")
