import logging
from typing import Literal


class LevelFileHandler(logging.Handler):
    """
    Кастомный обработчик логов, записывающий сообщения в разные файлы в зависимости от уровня лога

    Attributes:
        filename (str): Текущий путь к файлу логов (изменяется при emit)
        mode (str): Режим работы с файлом
    """

    def __init__(
        self, filename: str, mode: Literal["r", "rb", "w", "wb", "a", "ab"] = "a"
    ) -> None:
        super().__init__()
        self.filename = filename
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        """
        Обрабатывает и записывает лог-запись в соответствующий файл

        Args:
           record (logging.LogRecord): Объект записи лога, содержащий всю информацию о сообщении
        """

        if record.levelname == "WARNING":
            self.filename = "app/logger/log_files/calc_warning.log"
        elif record.exc_info:
            self.filename = "app/logger/log_files/calc_exception.log"
        elif record.levelname == "ERROR":
            self.filename = "app/logger/log_files/calc_error.log"

        msg = self.format(record)

        with open(self.filename, mode=self.mode) as file:
            file.write(msg + "\n")


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "handlers": {
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filename": "app/logger/log_files/logger.log",
            "mode": "a",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
    },
    "loggers": {"logger": {"handlers": ["file", "console"], "level": "DEBUG"}},
}
